use std::collections::HashMap;
use std::fs;
use std::io::{BufReader, Cursor};
use std::path::{Path, PathBuf};

use crate::formats::is_raw_file;
use crate::image_processing::ImageMetadata;
use chrono::{DateTime, NaiveDateTime, Utc};
use exif::{Exif, In, Value};
use little_exif::exif_tag::ExifTag;
use little_exif::filetype::FileExtension;
use little_exif::ifd::ExifTagGroup;
use little_exif::metadata::Metadata;
use little_exif::rational::{iR64, uR64};
use rawler::decoders::RawMetadata;

pub fn truncate_large_exif(value: &str) -> String {
    if value.len() <= 500 {
        return value.to_string();
    }

    let mut start_idx = 200;
    while !value.is_char_boundary(start_idx) {
        start_idx -= 1;
    }

    let mut end_idx = value.len() - 200;
    while !value.is_char_boundary(end_idx) {
        end_idx += 1;
    }

    if start_idx < end_idx {
        let start_str = &value[..start_idx];
        let end_str = &value[end_idx..];
        return format!("{}...{}", start_str, end_str);
    }

    value.to_string()
}

pub fn load_sidecar(sidecar_path: &Path) -> ImageMetadata {
    if !sidecar_path.exists() {
        return ImageMetadata::default();
    }

    let Ok(content) = fs::read_to_string(sidecar_path) else {
        return ImageMetadata::default();
    };

    let mut meta = serde_json::from_str::<ImageMetadata>(&content).unwrap_or_default();
    let mut healed = false;

    if let Some(ref mut exif_map) = meta.exif {
        for val in exif_map.values_mut() {
            if val.len() > 500 {
                *val = truncate_large_exif(val);
                healed = true;
            }
        }
    }

    if healed && let Ok(json) = serde_json::to_string_pretty(&meta) {
        let _ = fs::write(sidecar_path, json);
        log::info!(
            "Auto-healed bloated sidecar for: {}",
            sidecar_path.display()
        );
    }

    meta
}

fn to_ur64(val: &exif::Rational) -> uR64 {
    uR64 {
        nominator: val.num,
        denominator: val.denom,
    }
}

fn to_ir64(val: &exif::SRational) -> iR64 {
    iR64 {
        nominator: val.num,
        denominator: val.denom,
    }
}

fn clean_creation_datetime_str(s: &str) -> &str {
    s.trim().trim_matches('"').trim_matches('\'').trim()
}

fn fmt_date_str(s: String) -> String {
    if let Some(dt) = parse_creation_datetime(&s) {
        return dt.format("%Y-%m-%d %H:%M:%S").to_string();
    }
    clean_creation_datetime_str(&s).to_string()
}

fn normalize_creation_datetime(s: &str) -> Option<String> {
    let normalized = s.replace('T', " ");
    let (date, time) = normalized.split_once(' ')?;
    Some(format!("{} {}", date.replace(':', "-"), time))
}

fn parse_creation_datetime(s: &str) -> Option<NaiveDateTime> {
    let clean = clean_creation_datetime_str(s);
    if clean.is_empty() {
        return None;
    }

    let normalized = normalize_creation_datetime(clean);
    for candidate in std::iter::once(clean).chain(normalized.as_deref()) {
        for format in [
            "%Y:%m:%d %H:%M:%S",
            "%Y:%m:%d %H:%M:%S%.f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S%.f",
        ] {
            if let Ok(dt) = NaiveDateTime::parse_from_str(candidate, format) {
                return Some(dt);
            }
        }
    }

    None
}

fn parse_creation_field(field: &exif::Field) -> Option<DateTime<Utc>> {
    parse_creation_datetime(&field.display_value().to_string())
        .map(|dt| DateTime::from_naive_utc_and_offset(dt, Utc))
}

fn parse_raw_creation_date(date_str: Option<&str>) -> Option<DateTime<Utc>> {
    parse_creation_datetime(date_str?).map(|dt| DateTime::from_naive_utc_and_offset(dt, Utc))
}

pub fn read_exif(file_bytes: &[u8]) -> Option<Exif> {
    let exifreader = exif::Reader::new();
    exifreader
        .read_from_container(&mut Cursor::new(file_bytes))
        .ok()
}

pub fn read_raw_metadata(file_bytes: &[u8]) -> Option<RawMetadata> {
    let loader = rawler::RawLoader::new();
    let raw_source = rawler::rawsource::RawSource::new_from_slice(file_bytes);
    let decoder = loader.get_decoder(&raw_source).ok()?;
    decoder.raw_metadata(&raw_source, &Default::default()).ok()
}

pub fn read_exposure_time_secs(path: &str, file_bytes: &[u8]) -> Option<f32> {
    if let Some(map) = read_rrexif_sidecar(Path::new(path))
        && let Some(val_str) = map.get("ExposureTime").or(map.get("ShutterSpeedValue"))
    {
        let cleaned = val_str.replace(" s", "");
        if cleaned.contains('/') {
            let parts: Vec<&str> = cleaned.split('/').collect();
            if parts.len() == 2
                && let (Ok(num), Ok(den)) = (parts[0].parse::<f32>(), parts[1].parse::<f32>())
                && den != 0.0
            {
                return Some(num / den);
            }
        } else if let Ok(val) = cleaned.parse::<f32>() {
            return Some(val);
        }
    }

    if is_raw_file(path)
        && let Some(meta) = read_raw_metadata(file_bytes)
    {
        if let Some(r) = meta.exif.exposure_time {
            return if r.d == 0 {
                None
            } else {
                Some(r.n as f32 / r.d as f32)
            };
        } else if let Some(r) = meta.exif.shutter_speed_value {
            return if r.d == 0 {
                None
            } else {
                Some(r.n as f32 / r.d as f32)
            };
        }
    }

    if let Some(exif) = read_exif(file_bytes) {
        if let Some(exposure) = exif.get_field(exif::Tag::ExposureTime, In::PRIMARY) {
            if let Value::Rational(ref r) = exposure.value {
                if r.is_empty() {
                    return None;
                }

                let val = r.first()?;

                return if val.denom == 0 {
                    None
                } else {
                    Some(val.num as f32 / val.denom as f32)
                };
            }
        } else if let Some(shutter_speed) =
            exif.get_field(exif::Tag::ShutterSpeedValue, In::PRIMARY)
            && let Value::Rational(ref r) = shutter_speed.value
        {
            if r.is_empty() {
                return None;
            }

            let val = r.first()?;

            return if val.denom == 0 {
                None
            } else {
                Some(val.num as f32 / val.denom as f32)
            };
        }
    }
    None
}

pub fn read_iso(path: &str, file_bytes: &[u8]) -> Option<u32> {
    if let Some(map) = read_rrexif_sidecar(Path::new(path))
        && let Some(val_str) = map
            .get("ISOSpeed")
            .or(map.get("PhotographicSensitivity"))
            .or(map.get("ISOSpeedRatings"))
        && let Ok(val) = val_str.parse::<u32>()
    {
        return Some(val);
    }

    if is_raw_file(path)
        && let Some(meta) = read_raw_metadata(file_bytes)
    {
        if let Some(r) = meta.exif.iso_speed {
            return Some(r);
        } else if let Some(r) = meta.exif.iso_speed_ratings {
            return Some(r as u32);
        }
    }

    if let Some(exif) = read_exif(file_bytes) {
        if let Some(r) = exif.get_field(exif::Tag::ISOSpeed, In::PRIMARY) {
            return r.value.get_uint(0);
        } else if let Some(r) = exif.get_field(exif::Tag::PhotographicSensitivity, In::PRIMARY) {
            return r.value.get_uint(0);
        }
    }
    None
}

pub fn extract_metadata(file_bytes: &[u8]) -> Option<HashMap<String, String>> {
    let mut map = HashMap::new();

    if let Some(exif_obj) = read_exif(file_bytes) {
        for field in exif_obj.fields() {
            match field.tag {
                exif::Tag::ExposureTime => {
                    if let exif::Value::Rational(ref v) = field.value
                        && !v.is_empty()
                    {
                        let r = &v[0];
                        if r.num == 1 && r.denom > 1 {
                            map.insert("ExposureTime".to_string(), format!("1/{} s", r.denom));
                        } else {
                            let val = r.num as f32 / r.denom as f32;
                            if val < 1.0 && val > 0.0 {
                                map.insert(
                                    "ExposureTime".to_string(),
                                    format!("1/{} s", (1.0 / val).round()),
                                );
                            } else {
                                map.insert("ExposureTime".to_string(), format!("{} s", val));
                            }
                        }
                    }
                }
                exif::Tag::ShutterSpeedValue => {
                    if let exif::Value::SRational(ref v) = field.value
                        && !v.is_empty()
                    {
                        let val = v[0].num as f32 / v[0].denom as f32;
                        map.insert("ShutterSpeedValue".to_string(), val.to_string());
                    }
                }
                exif::Tag::FNumber => {
                    if let exif::Value::Rational(ref v) = field.value
                        && !v.is_empty()
                    {
                        let val = v[0].num as f32 / v[0].denom as f32;
                        map.insert("FNumber".to_string(), format!("f/{}", val));
                    }
                }
                exif::Tag::ApertureValue => {
                    if let exif::Value::Rational(ref v) = field.value
                        && !v.is_empty()
                    {
                        let val = v[0].num as f32 / v[0].denom as f32;
                        map.insert("ApertureValue".to_string(), format!("f/{}", val));
                    }
                }
                exif::Tag::FocalLength => {
                    if let exif::Value::Rational(ref v) = field.value
                        && !v.is_empty()
                    {
                        let val = v[0].num as f32 / v[0].denom as f32;
                        map.insert("FocalLength".to_string(), val.to_string());
                        map.insert("FocalLengthIn35mmFilm".to_string(), val.to_string());
                    }
                }
                exif::Tag::PhotographicSensitivity | exif::Tag::ISOSpeed => {
                    map.insert(
                        "PhotographicSensitivity".to_string(),
                        field.display_value().to_string(),
                    );
                    map.insert("ISOSpeed".to_string(), field.display_value().to_string());
                }
                exif::Tag::DateTimeOriginal => {
                    map.insert(
                        "DateTimeOriginal".to_string(),
                        fmt_date_str(field.display_value().to_string()),
                    );
                }
                exif::Tag::DateTime => {
                    map.insert(
                        "CreateDate".to_string(),
                        fmt_date_str(field.display_value().to_string()),
                    );
                }
                exif::Tag::DateTimeDigitized => {
                    map.insert(
                        "ModifyDate".to_string(),
                        fmt_date_str(field.display_value().to_string()),
                    );
                }
                _ => {
                    let val = field.display_value().with_unit(&exif_obj).to_string();
                    if !val.trim().is_empty() {
                        map.insert(field.tag.to_string(), val);
                    }
                }
            }
        }
    }

    if !map.is_empty() {
        return Some(map);
    }

    let metadata = read_raw_metadata(file_bytes)?;

    let exif = metadata.exif;

    let fmt_rat = |r: &rawler::formats::tiff::Rational| -> f32 {
        if r.d == 0 {
            0.0
        } else {
            r.n as f32 / r.d as f32
        }
    };

    let fmt_srat = |r: &rawler::formats::tiff::SRational| -> f32 {
        if r.d == 0 {
            0.0
        } else {
            r.n as f32 / r.d as f32
        }
    };

    let mut insert_if_present = |key: &str, val: String| {
        let trimmed = val.trim();
        if !trimmed.is_empty() {
            map.insert(key.to_string(), truncate_large_exif(trimmed));
        }
    };

    insert_if_present("Make", metadata.make);
    insert_if_present("Model", metadata.model);

    if let Some(v) = exif.artist {
        insert_if_present("Artist", v);
    }
    if let Some(v) = exif.copyright {
        insert_if_present("Copyright", v);
    }
    if let Some(v) = exif.owner_name {
        insert_if_present("OwnerName", v);
    }
    if let Some(v) = exif.serial_number {
        insert_if_present("SerialNumber", v);
    }
    if let Some(v) = exif.image_number {
        insert_if_present("ImageNumber", v.to_string());
    }
    if let Some(v) = exif.user_comment {
        insert_if_present("UserComment", v);
    }

    if let Some(v) = exif.date_time_original {
        insert_if_present("DateTimeOriginal", fmt_date_str(v));
    }
    if let Some(v) = exif.create_date {
        insert_if_present("CreateDate", fmt_date_str(v));
    }
    if let Some(v) = exif.modify_date {
        insert_if_present("ModifyDate", fmt_date_str(v));
    }

    if let Some(v) = exif.offset_time {
        insert_if_present("OffsetTime", v);
    }
    if let Some(v) = exif.offset_time_original {
        insert_if_present("OffsetTimeOriginal", v);
    }
    if let Some(v) = exif.offset_time_digitized {
        insert_if_present("OffsetTimeDigitized", v);
    }
    if let Some(v) = exif.sub_sec_time {
        insert_if_present("SubSecTime", v);
    }
    if let Some(v) = exif.sub_sec_time_original {
        insert_if_present("SubSecTimeOriginal", v);
    }
    if let Some(v) = exif.sub_sec_time_digitized {
        insert_if_present("SubSecTimeDigitized", v);
    }

    if let Some(v) = exif.lens_model {
        insert_if_present("LensModel", v);
    } else if let Some(lens_desc) = &metadata.lens {
        insert_if_present("LensModel", lens_desc.lens_model.clone());
    }

    if let Some(v) = exif.lens_make {
        insert_if_present("LensMake", v);
    } else if let Some(lens_desc) = &metadata.lens {
        insert_if_present("LensMake", lens_desc.lens_make.clone());
    }

    if let Some(v) = exif.lens_serial_number {
        insert_if_present("LensSerialNumber", v);
    }

    if let Some(v) = exif.orientation {
        insert_if_present("Orientation", v.to_string());
    }

    if let Some(r) = exif.fnumber {
        let val = fmt_rat(&r);
        insert_if_present("FNumber", format!("f/{}", val));
    }

    if let Some(r) = exif.aperture_value {
        let val = fmt_rat(&r);
        insert_if_present("ApertureValue", format!("f/{}", val));
    }

    if let Some(r) = exif.max_aperture_value {
        insert_if_present("MaxApertureValue", fmt_rat(&r).to_string());
    }

    if let Some(r) = exif.exposure_time {
        if r.n == 1 && r.d > 1 {
            insert_if_present("ExposureTime", format!("1/{} s", r.d));
        } else {
            let val = fmt_rat(&r);
            if val < 1.0 && val > 0.0 {
                insert_if_present("ExposureTime", format!("1/{} s", (1.0 / val).round()));
            } else {
                insert_if_present("ExposureTime", format!("{} s", val));
            }
        }
    }

    if let Some(r) = exif.shutter_speed_value {
        insert_if_present("ShutterSpeedValue", fmt_srat(&r).to_string());
    }

    if let Some(v) = exif.iso_speed {
        insert_if_present("PhotographicSensitivity", v.to_string());
        insert_if_present("ISOSpeed", v.to_string());
    } else if let Some(v) = exif.iso_speed_ratings {
        insert_if_present("PhotographicSensitivity", v.to_string());
        insert_if_present("ISOSpeedRatings", v.to_string());
    }

    if let Some(v) = exif.recommended_exposure_index {
        insert_if_present("RecommendedExposureIndex", v.to_string());
    }
    if let Some(v) = exif.sensitivity_type {
        insert_if_present("SensitivityType", v.to_string());
    }

    if let Some(r) = exif.focal_length {
        let val = fmt_rat(&r);
        insert_if_present("FocalLength", val.to_string());
        insert_if_present("FocalLengthIn35mmFilm", val.to_string());
    }

    if let Some(r) = exif.exposure_bias {
        insert_if_present("ExposureBiasValue", fmt_srat(&r).to_string());
    }

    if let Some(v) = exif.metering_mode {
        insert_if_present("MeteringMode", v.to_string());
    }
    if let Some(v) = exif.light_source {
        insert_if_present("LightSource", v.to_string());
    }
    if let Some(v) = exif.flash {
        insert_if_present("Flash", v.to_string());
    }
    if let Some(v) = exif.white_balance {
        insert_if_present("WhiteBalance", v.to_string());
    }
    if let Some(v) = exif.exposure_program {
        insert_if_present("ExposureProgram", v.to_string());
    }
    if let Some(v) = exif.exposure_mode {
        insert_if_present("ExposureMode", v.to_string());
    }
    if let Some(v) = exif.scene_capture_type {
        insert_if_present("SceneCaptureType", v.to_string());
    }
    if let Some(v) = exif.color_space {
        insert_if_present("ColorSpace", v.to_string());
    }
    if let Some(r) = exif.flash_energy {
        insert_if_present("FlashEnergy", fmt_rat(&r).to_string());
    }
    if let Some(r) = exif.brightness_value {
        insert_if_present("BrightnessValue", fmt_srat(&r).to_string());
    }

    if let Some(r) = exif.subject_distance {
        insert_if_present("SubjectDistance", fmt_rat(&r).to_string());
    }
    if let Some(v) = exif.subject_distance_range {
        insert_if_present("SubjectDistanceRange", v.to_string());
    }

    if let Some(gps) = exif.gps {
        let fmt_gps_coord = |coords: &[rawler::formats::tiff::Rational; 3]| -> String {
            format!(
                "{} deg {} min {} sec",
                fmt_rat(&coords[0]),
                fmt_rat(&coords[1]),
                fmt_rat(&coords[2])
            )
        };

        if let Some(lat) = gps.gps_latitude {
            insert_if_present("GPSLatitude", fmt_gps_coord(&lat));
        }
        if let Some(lat_ref) = gps.gps_latitude_ref {
            insert_if_present("GPSLatitudeRef", lat_ref);
        }
        if let Some(lon) = gps.gps_longitude {
            insert_if_present("GPSLongitude", fmt_gps_coord(&lon));
        }
        if let Some(lon_ref) = gps.gps_longitude_ref {
            insert_if_present("GPSLongitudeRef", lon_ref);
        }
        if let Some(alt) = gps.gps_altitude {
            insert_if_present("GPSAltitude", fmt_rat(&alt).to_string());
        }
        if let Some(alt_ref) = gps.gps_altitude_ref {
            insert_if_present("GPSAltitudeRef", alt_ref.to_string());
        }
        if let Some(v) = gps.gps_img_direction {
            insert_if_present("GPSImgDirection", fmt_rat(&v).to_string());
        }
        if let Some(v) = gps.gps_img_direction_ref {
            insert_if_present("GPSImgDirectionRef", v);
        }
        if let Some(v) = gps.gps_speed {
            insert_if_present("GPSSpeed", fmt_rat(&v).to_string());
        }
        if let Some(v) = gps.gps_speed_ref {
            insert_if_present("GPSSpeedRef", v);
        }
        if let Some(v) = gps.gps_status {
            insert_if_present("GPSStatus", v);
        }
        if let Some(v) = gps.gps_measure_mode {
            insert_if_present("GPSMeasureMode", v);
        }
        if let Some(v) = gps.gps_dop {
            insert_if_present("GPSDOP", fmt_rat(&v).to_string());
        }
        if let Some(v) = gps.gps_map_datum {
            insert_if_present("GPSMapDatum", v);
        }
    }

    Some(map)
}

pub fn get_creation_date_from_path(path: &Path) -> DateTime<Utc> {
    if let Some(map) = read_rrexif_sidecar(path)
        && let Some(dt_str) = map.get("DateTimeOriginal").or(map.get("CreateDate"))
        && let Some(dt) = parse_creation_datetime(dt_str)
    {
        return DateTime::from_naive_utc_and_offset(dt, Utc);
    }

    if let Ok(file) = std::fs::File::open(path) {
        let mut bufreader = BufReader::new(&file);
        let exifreader = exif::Reader::new();

        if let Ok(exif_obj) = exifreader.read_from_container(&mut bufreader) {
            for tag in [exif::Tag::DateTimeOriginal, exif::Tag::DateTime] {
                if let Some(field) = exif_obj.get_field(tag, exif::In::PRIMARY)
                    && let Some(dt) = parse_creation_field(field)
                {
                    return dt;
                }
            }
        }
    }

    if is_raw_file(path.to_string_lossy().as_ref()) {
        let loader = rawler::RawLoader::new();
        if let Ok(raw_source) = rawler::rawsource::RawSource::new(path)
            && let Ok(decoder) = loader.get_decoder(&raw_source)
            && let Ok(metadata) = decoder.raw_metadata(&raw_source, &Default::default())
        {
            if let Some(dt) = parse_raw_creation_date(metadata.exif.date_time_original.as_deref()) {
                return dt;
            }
            if let Some(dt) = parse_raw_creation_date(metadata.exif.create_date.as_deref()) {
                return dt;
            }
        }
    }

    fs::metadata(path)
        .ok()
        .and_then(|m| m.created().ok())
        .map(DateTime::<Utc>::from)
        .unwrap_or_else(Utc::now)
}

#[cfg(target_os = "android")]
pub fn get_creation_date_from_bytes(path_hint: &str, file_bytes: &[u8]) -> DateTime<Utc> {
    if let Some(exif_obj) = read_exif(file_bytes) {
        for tag in [exif::Tag::DateTimeOriginal, exif::Tag::DateTime] {
            if let Some(field) = exif_obj.get_field(tag, exif::In::PRIMARY)
                && let Some(dt) = parse_creation_field(field)
            {
                return dt;
            }
        }
    }

    if is_raw_file(path_hint)
        && let Some(metadata) = read_raw_metadata(file_bytes)
    {
        if let Some(dt) = parse_raw_creation_date(metadata.exif.date_time_original.as_deref()) {
            return dt;
        }
        if let Some(dt) = parse_raw_creation_date(metadata.exif.create_date.as_deref()) {
            return dt;
        }
    }

    Utc::now()
}

// Copies the complete EXIF block (IFD0 and its sub-IFDs, including MakerNote
// and unknown tags) from the source file. IFD1 is skipped because it holds the
// original's thumbnail, which no longer matches the exported pixels.
fn copy_full_exif_from_source(
    metadata: &mut Metadata,
    original_path: &Path,
    strip_gps: bool,
) -> bool {
    let Ok(source_metadata) = Metadata::new_from_path(original_path) else {
        return false;
    };

    let mut copied_any = false;
    for ifd in source_metadata.get_ifds() {
        if ifd.get_generic_ifd_nr() != 0 {
            continue;
        }
        if strip_gps && ifd.get_ifd_type() == ExifTagGroup::GPS {
            continue;
        }
        for tag in ifd.get_tags() {
            metadata.set_tag(tag.clone());
            copied_any = true;
        }
    }
    copied_any
}

// The metadata panel edits (title, author, copyright, comments) only live in
// the sidecar, so they take precedence over the values copied from the source
// file. A key that is missing from the sidecar was cleared by the user.
fn apply_sidecar_field_overrides(metadata: &mut Metadata, map: &HashMap<String, String>) {
    let clean_s = |s: &String| s.replace('"', "").trim().to_string();
    // Values that clean down to nothing or to the "..." marker left behind by
    // truncate_large_exif are not user edits, so the value copied from the
    // source file is kept for those.
    let is_user_edit = |s: &str| !s.is_empty() && s != "...";

    match map.get("Artist").map(clean_s) {
        Some(val) => {
            if is_user_edit(&val) {
                metadata.set_tag(ExifTag::Artist(val));
            }
        }
        None => {
            metadata.remove_tag(ExifTag::Artist(String::new()));
        }
    }
    match map.get("Copyright").map(clean_s) {
        Some(val) => {
            if is_user_edit(&val) {
                metadata.set_tag(ExifTag::Copyright(val));
            }
        }
        None => {
            metadata.remove_tag(ExifTag::Copyright(String::new()));
        }
    }
    match map.get("ImageDescription").map(clean_s) {
        Some(val) => {
            if is_user_edit(&val) {
                metadata.set_tag(ExifTag::ImageDescription(val));
            }
        }
        None => {
            metadata.remove_tag(ExifTag::ImageDescription(String::new()));
        }
    }
    match map.get("UserComment").map(clean_s) {
        Some(val) => {
            // Unedited sidecars store kamadak-exif's hex dump of the original
            // UserComment bytes; only write back plain-text (i.e. user-entered)
            // values and otherwise keep the bytes copied from the source.
            if is_user_edit(&val) && !val.starts_with("0x") {
                metadata.set_tag(ExifTag::UserComment(val.into_bytes()));
            }
        }
        None => {
            metadata.remove_tag(ExifTag::UserComment(Vec::new()));
        }
    }
}

pub fn write_image_with_metadata(
    image_bytes: &mut Vec<u8>,
    original_path_str: &str,
    output_format: &str,
    keep_metadata: bool,
    strip_gps: bool,
) -> Result<(), String> {
    // FIXME: temporary solution until I find a way to write metadata to TIFF
    if !keep_metadata || output_format.to_lowercase() == "tiff" {
        return Ok(());
    }

    let original_path = Path::new(original_path_str);
    if !original_path.exists() {
        return Ok(());
    }

    // Skip TIFF sources to avoid potential tag corruption issues
    let original_ext = original_path
        .extension()
        .and_then(|s| s.to_str())
        .unwrap_or("")
        .to_lowercase();
    if original_ext == "tiff" || original_ext == "tif" {
        return Ok(());
    }

    let file_type = match output_format.to_lowercase().as_str() {
        "jpg" | "jpeg" => FileExtension::JPEG,
        "png" => FileExtension::PNG {
            as_zTXt_chunk: true,
        },
        "tiff" => FileExtension::TIFF,
        "webp" => FileExtension::WEBP,
        _ => return Ok(()),
    };

    let mut metadata = Metadata::new();

    // Prefer copying the complete EXIF block from the source file: the sidecar
    // only carries a display-formatted subset of the tags, which used to drop
    // most of the metadata from exports (issue #1165).
    let full_exif_copied = !is_raw_file(original_path_str)
        && copy_full_exif_from_source(&mut metadata, original_path, strip_gps);
    let mut source_read_success = full_exif_copied;

    if !source_read_success && let Some(map) = read_rrexif_sidecar(original_path) {
        source_read_success = true;

        let clean_s = |s: &String| s.replace('"', "").trim().to_string();

        let parse_ur64 = |s: &str| -> Option<uR64> {
            let cleaned_string = s
                .replace("f/", "")
                .replace(" s", "")
                .replace(" mm", "")
                .replace("\"", "");

            let val = cleaned_string.trim();

            if val.contains('/') {
                let parts: Vec<&str> = val.split('/').collect();
                if parts.len() == 2
                    && let (Ok(n), Ok(d)) = (parts[0].parse::<u32>(), parts[1].parse::<u32>())
                {
                    return Some(uR64 {
                        nominator: n,
                        denominator: d,
                    });
                }
            } else if let Ok(f) = val.parse::<f32>() {
                return Some(uR64 {
                    nominator: (f * 1000.0) as u32,
                    denominator: 1000,
                });
            }
            None
        };
        if let Some(val) = map.get("Make") {
            metadata.set_tag(ExifTag::Make(clean_s(val)));
        }
        if let Some(val) = map.get("Model") {
            metadata.set_tag(ExifTag::Model(clean_s(val)));
        }
        if let Some(val) = map.get("LensMake") {
            metadata.set_tag(ExifTag::LensMake(clean_s(val)));
        }
        if let Some(val) = map.get("LensModel") {
            metadata.set_tag(ExifTag::LensModel(clean_s(val)));
        }
        if let Some(val) = map.get("Artist") {
            metadata.set_tag(ExifTag::Artist(clean_s(val)));
        }
        if let Some(val) = map.get("Copyright") {
            metadata.set_tag(ExifTag::Copyright(clean_s(val)));
        }
        if let Some(val) = map.get("UserComment") {
            metadata.set_tag(ExifTag::UserComment(clean_s(val).into_bytes()));
        }
        if let Some(val) = map.get("ImageDescription") {
            metadata.set_tag(ExifTag::ImageDescription(clean_s(val)));
        }
        if let Some(val) = map.get("DateTimeOriginal") {
            metadata.set_tag(ExifTag::DateTimeOriginal(clean_s(val)));
        }
        if let Some(val) = map.get("CreateDate") {
            metadata.set_tag(ExifTag::CreateDate(clean_s(val)));
        }
        if let Some(val) = map.get("FNumber")
            && let Some(ur) = parse_ur64(val)
        {
            metadata.set_tag(ExifTag::FNumber(vec![ur]));
        }
        if let Some(val) = map.get("ExposureTime")
            && let Some(ur) = parse_ur64(val)
        {
            metadata.set_tag(ExifTag::ExposureTime(vec![ur]));
        }
        if let Some(val) = map.get("FocalLength")
            && let Some(ur) = parse_ur64(val)
        {
            metadata.set_tag(ExifTag::FocalLength(vec![ur]));
        }
        if let Some(val) = map.get("FocalLengthIn35mmFilm") {
            let cleaned = val.replace(" mm", "").replace("\"", "");
            let trimmed = cleaned.trim();
            if let Ok(f_val) = trimmed.parse::<f32>() {
                metadata.set_tag(ExifTag::FocalLengthIn35mmFormat(vec![f_val.round() as u16]));
            }
        }
        if let Some(val) = map.get("ISOSpeed").or(map.get("PhotographicSensitivity"))
            && let Ok(iso) = val.replace('"', "").trim().parse::<u16>()
        {
            metadata.set_tag(ExifTag::ISO(vec![iso]));
        }
    }

    if !source_read_success && let Ok(file) = std::fs::File::open(original_path) {
        let mut bufreader = std::io::BufReader::new(&file);
        let exifreader = exif::Reader::new();

        if let Ok(exif_obj) = exifreader.read_from_container(&mut bufreader) {
            source_read_success = true;

            let get_string_val = |field: &exif::Field| -> String {
                match &field.value {
                    exif::Value::Ascii(vec) => vec
                        .iter()
                        .map(|v| {
                            String::from_utf8_lossy(v)
                                .trim_matches(char::from(0))
                                .to_string()
                        })
                        .collect::<Vec<String>>()
                        .join(" "),
                    _ => field
                        .display_value()
                        .to_string()
                        .replace("\"", "")
                        .trim()
                        .to_string(),
                }
            };

            if let Some(f) = exif_obj.get_field(exif::Tag::Make, exif::In::PRIMARY) {
                metadata.set_tag(ExifTag::Make(get_string_val(f)));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::Model, exif::In::PRIMARY) {
                metadata.set_tag(ExifTag::Model(get_string_val(f)));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::LensMake, exif::In::PRIMARY) {
                metadata.set_tag(ExifTag::LensMake(get_string_val(f)));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::LensModel, exif::In::PRIMARY) {
                metadata.set_tag(ExifTag::LensModel(get_string_val(f)));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::Artist, exif::In::PRIMARY) {
                metadata.set_tag(ExifTag::Artist(get_string_val(f)));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::Copyright, exif::In::PRIMARY) {
                metadata.set_tag(ExifTag::Copyright(get_string_val(f)));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::DateTimeOriginal, exif::In::PRIMARY) {
                metadata.set_tag(ExifTag::DateTimeOriginal(get_string_val(f)));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::DateTime, exif::In::PRIMARY) {
                metadata.set_tag(ExifTag::CreateDate(get_string_val(f)));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::FNumber, exif::In::PRIMARY)
                && let exif::Value::Rational(v) = &f.value
                && !v.is_empty()
            {
                metadata.set_tag(ExifTag::FNumber(vec![to_ur64(&v[0])]));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::ExposureTime, exif::In::PRIMARY)
                && let exif::Value::Rational(v) = &f.value
                && !v.is_empty()
            {
                metadata.set_tag(ExifTag::ExposureTime(vec![to_ur64(&v[0])]));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::FocalLength, exif::In::PRIMARY)
                && let exif::Value::Rational(v) = &f.value
                && !v.is_empty()
            {
                metadata.set_tag(ExifTag::FocalLength(vec![to_ur64(&v[0])]));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::ExposureBiasValue, exif::In::PRIMARY) {
                match &f.value {
                    exif::Value::SRational(v) if !v.is_empty() => {
                        metadata.set_tag(ExifTag::ExposureCompensation(vec![to_ir64(&v[0])]));
                    }
                    exif::Value::Rational(v) if !v.is_empty() => {
                        metadata.set_tag(ExifTag::ExposureCompensation(vec![iR64 {
                            nominator: v[0].num as i32,
                            denominator: v[0].denom as i32,
                        }]));
                    }
                    _ => {}
                }
            }
            if let Some(f) =
                exif_obj.get_field(exif::Tag::PhotographicSensitivity, exif::In::PRIMARY)
            {
                if let Some(val) = f.value.get_uint(0) {
                    metadata.set_tag(ExifTag::ISO(vec![val as u16]));
                }
            } else if let Some(f) = exif_obj.get_field(exif::Tag::ISOSpeed, exif::In::PRIMARY)
                && let Some(val) = f.value.get_uint(0)
            {
                metadata.set_tag(ExifTag::ISO(vec![val as u16]));
            }
            if let Some(f) = exif_obj.get_field(exif::Tag::FocalLengthIn35mmFilm, exif::In::PRIMARY)
                && let Some(val) = f.value.get_uint(0)
            {
                metadata.set_tag(ExifTag::FocalLengthIn35mmFormat(vec![val as u16]));
            }
            if !strip_gps {
                if let Some(f) = exif_obj.get_field(exif::Tag::GPSLatitude, exif::In::PRIMARY)
                    && let exif::Value::Rational(v) = &f.value
                    && v.len() >= 3
                {
                    metadata.set_tag(ExifTag::GPSLatitude(vec![
                        to_ur64(&v[0]),
                        to_ur64(&v[1]),
                        to_ur64(&v[2]),
                    ]));
                }
                if let Some(f) = exif_obj.get_field(exif::Tag::GPSLatitudeRef, exif::In::PRIMARY) {
                    metadata.set_tag(ExifTag::GPSLatitudeRef(get_string_val(f)));
                }
                if let Some(f) = exif_obj.get_field(exif::Tag::GPSLongitude, exif::In::PRIMARY)
                    && let exif::Value::Rational(v) = &f.value
                    && v.len() >= 3
                {
                    metadata.set_tag(ExifTag::GPSLongitude(vec![
                        to_ur64(&v[0]),
                        to_ur64(&v[1]),
                        to_ur64(&v[2]),
                    ]));
                }
                if let Some(f) = exif_obj.get_field(exif::Tag::GPSLongitudeRef, exif::In::PRIMARY) {
                    metadata.set_tag(ExifTag::GPSLongitudeRef(get_string_val(f)));
                }
                if let Some(f) = exif_obj.get_field(exif::Tag::GPSAltitude, exif::In::PRIMARY)
                    && let exif::Value::Rational(v) = &f.value
                    && !v.is_empty()
                {
                    metadata.set_tag(ExifTag::GPSAltitude(vec![to_ur64(&v[0])]));
                }
                if let Some(f) = exif_obj.get_field(exif::Tag::GPSAltitudeRef, exif::In::PRIMARY) {
                    let alt_ref = f.value.get_uint(0).unwrap_or(0) as u8;
                    metadata.set_tag(ExifTag::GPSAltitudeRef(vec![alt_ref]));
                }
            }
        }
    }

    if !source_read_success && is_raw_file(original_path_str) {
        let loader = rawler::RawLoader::new();
        if let Ok(raw_source) = rawler::rawsource::RawSource::new(Path::new(original_path_str))
            && let Ok(decoder) = loader.get_decoder(&raw_source)
            && let Ok(meta) = decoder.raw_metadata(&raw_source, &Default::default())
        {
            if !meta.make.is_empty() {
                metadata.set_tag(ExifTag::Make(meta.make.clone()));
            }
            if !meta.model.is_empty() {
                metadata.set_tag(ExifTag::Model(meta.model.clone()));
            }
            let exif = meta.exif;
            if let Some(artist) = exif.artist {
                metadata.set_tag(ExifTag::Artist(artist));
            }
            if let Some(copyright) = exif.copyright {
                metadata.set_tag(ExifTag::Copyright(copyright));
            }
            if let Some(dt) = exif.date_time_original {
                metadata.set_tag(ExifTag::DateTimeOriginal(dt));
            }
            if let Some(dt) = exif.create_date {
                metadata.set_tag(ExifTag::CreateDate(dt));
            }
            if let Some(lens_make) = exif.lens_make {
                metadata.set_tag(ExifTag::LensMake(lens_make));
            }
            if let Some(lens_model) = exif.lens_model {
                metadata.set_tag(ExifTag::LensModel(lens_model));
            }
            if let Some(f) = exif.fnumber {
                metadata.set_tag(ExifTag::FNumber(vec![uR64 {
                    nominator: f.n,
                    denominator: f.d,
                }]));
            }
            if let Some(t) = exif.exposure_time {
                metadata.set_tag(ExifTag::ExposureTime(vec![uR64 {
                    nominator: t.n,
                    denominator: t.d,
                }]));
            }
            if let Some(fl) = exif.focal_length {
                metadata.set_tag(ExifTag::FocalLength(vec![uR64 {
                    nominator: fl.n,
                    denominator: fl.d,
                }]));
            }
            if let Some(iso) = exif.iso_speed {
                metadata.set_tag(ExifTag::ISO(vec![iso as u16]));
            } else if let Some(iso) = exif.iso_speed_ratings {
                metadata.set_tag(ExifTag::ISO(vec![iso]));
            }
            if let Some(ev) = exif.exposure_bias {
                metadata.set_tag(ExifTag::ExposureCompensation(vec![iR64 {
                    nominator: ev.n,
                    denominator: ev.d,
                }]));
            }
            if let Some(flash) = exif.flash {
                metadata.set_tag(ExifTag::Flash(vec![flash]));
            }
            if let Some(metering) = exif.metering_mode {
                metadata.set_tag(ExifTag::MeteringMode(vec![metering]));
            }
            if let Some(wb) = exif.white_balance {
                metadata.set_tag(ExifTag::WhiteBalance(vec![wb]));
            }
            if let Some(prog) = exif.exposure_program {
                metadata.set_tag(ExifTag::ExposureProgram(vec![prog]));
            }
            if !strip_gps && let Some(gps) = exif.gps {
                if let Some(lat) = gps.gps_latitude {
                    metadata.set_tag(ExifTag::GPSLatitude(vec![
                        uR64 {
                            nominator: lat[0].n,
                            denominator: lat[0].d,
                        },
                        uR64 {
                            nominator: lat[1].n,
                            denominator: lat[1].d,
                        },
                        uR64 {
                            nominator: lat[2].n,
                            denominator: lat[2].d,
                        },
                    ]));
                }
                if let Some(lat_ref) = gps.gps_latitude_ref {
                    metadata.set_tag(ExifTag::GPSLatitudeRef(lat_ref));
                }
                if let Some(lon) = gps.gps_longitude {
                    metadata.set_tag(ExifTag::GPSLongitude(vec![
                        uR64 {
                            nominator: lon[0].n,
                            denominator: lon[0].d,
                        },
                        uR64 {
                            nominator: lon[1].n,
                            denominator: lon[1].d,
                        },
                        uR64 {
                            nominator: lon[2].n,
                            denominator: lon[2].d,
                        },
                    ]));
                }
                if let Some(lon_ref) = gps.gps_longitude_ref {
                    metadata.set_tag(ExifTag::GPSLongitudeRef(lon_ref));
                }
                if let Some(alt) = gps.gps_altitude {
                    metadata.set_tag(ExifTag::GPSAltitude(vec![uR64 {
                        nominator: alt.n,
                        denominator: alt.d,
                    }]));
                }
                if let Some(alt_ref) = gps.gps_altitude_ref {
                    metadata.set_tag(ExifTag::GPSAltitudeRef(vec![alt_ref]));
                }
            }
        }
    }

    if full_exif_copied && let Some(map) = read_rrexif_sidecar(original_path) {
        apply_sidecar_field_overrides(&mut metadata, &map);
    }

    metadata.set_tag(ExifTag::Software("RapidRAW".to_string()));
    metadata.set_tag(ExifTag::Orientation(vec![1u16]));
    metadata.set_tag(ExifTag::ColorSpace(vec![1u16]));

    // The export has any rotation baked into the pixels, so the dimension tags
    // copied from the source may be stale.
    if let Ok(reader) =
        image::ImageReader::new(Cursor::new(image_bytes.as_slice())).with_guessed_format()
        && let Ok((width, height)) = reader.into_dimensions()
    {
        metadata.set_tag(ExifTag::ExifImageWidth(vec![width]));
        metadata.set_tag(ExifTag::ExifImageHeight(vec![height]));
    }

    if let Err(e) = metadata.write_to_vec(image_bytes, file_type) {
        log::warn!("Failed to write metadata: {}", e);
    }

    Ok(())
}

pub fn get_primary_sidecar_path(image_path: &Path) -> PathBuf {
    let mut filename = image_path.file_name().unwrap_or_default().to_os_string();
    filename.push(".rrdata");
    image_path.with_file_name(filename)
}

pub fn get_rrexif_path(image_path: &Path) -> PathBuf {
    let mut filename = image_path.file_name().unwrap_or_default().to_os_string();
    filename.push(".rrexif");
    image_path.with_file_name(filename)
}

fn load_primary_metadata(image_path: &Path) -> ImageMetadata {
    let primary = get_primary_sidecar_path(image_path);
    load_sidecar(&primary)
}

fn save_primary_metadata(image_path: &Path, metadata: &ImageMetadata) -> std::io::Result<()> {
    let primary = get_primary_sidecar_path(image_path);
    let json = serde_json::to_string_pretty(metadata).map_err(std::io::Error::other)?;
    fs::write(&primary, json)
}

pub fn read_rrexif_sidecar(image_path: &Path) -> Option<HashMap<String, String>> {
    let metadata = load_primary_metadata(image_path);
    if let Some(exif) = metadata.exif {
        return Some(exif);
    }

    let legacy = get_rrexif_path(image_path);
    if legacy.exists()
        && let Ok(content) = fs::read_to_string(&legacy)
        && let Ok(map) = serde_json::from_str::<HashMap<String, String>>(&content)
    {
        let mut migrated = load_primary_metadata(image_path);
        migrated.exif = Some(map.clone());
        if save_primary_metadata(image_path, &migrated).is_ok() {
            let _ = fs::remove_file(&legacy);
        }
        return Some(map);
    }

    None
}

pub fn read_exif_data_from_bytes(path: &str, file_bytes: &[u8]) -> HashMap<String, String> {
    if is_raw_file(path)
        && let Some(map) = extract_metadata(file_bytes)
    {
        return map;
    }

    let mut exif_data = HashMap::new();
    if let Some(exif) = read_exif(file_bytes) {
        for field in exif.fields() {
            let raw_val = field.display_value().with_unit(&exif).to_string();
            exif_data.insert(field.tag.to_string(), truncate_large_exif(&raw_val));
        }
    }
    exif_data
}

pub fn read_exif_data(path: &str, file_bytes: &[u8]) -> HashMap<String, String> {
    let source_path = Path::new(path);
    if let Some(sidecar_exif) = read_rrexif_sidecar(source_path) {
        return sidecar_exif;
    }

    let exif_map = read_exif_data_from_bytes(path, file_bytes);
    if !exif_map.is_empty() {
        let mut metadata = load_primary_metadata(source_path);
        metadata.exif = Some(exif_map.clone());
        let _ = save_primary_metadata(source_path, &metadata);
    }
    exif_map
}

pub fn persist_exif_if_missing(source_path: &Path, source_path_str: &str, file_bytes: &[u8]) {
    {
        let metadata = load_primary_metadata(source_path);
        if metadata.exif.is_some() {
            return;
        }
    }

    let legacy = get_rrexif_path(source_path);
    if legacy.exists()
        && let Ok(content) = fs::read_to_string(&legacy)
        && let Ok(map) = serde_json::from_str::<HashMap<String, String>>(&content)
    {
        let mut metadata = load_primary_metadata(source_path);
        metadata.exif = Some(map);
        if save_primary_metadata(source_path, &metadata).is_ok() {
            let _ = fs::remove_file(&legacy);
        }
        return;
    }

    let exif_map = read_exif_data_from_bytes(source_path_str, file_bytes);
    if exif_map.is_empty() {
        return;
    }

    let mut metadata = load_primary_metadata(source_path);

    if metadata.exif.is_none() {
        metadata.exif = Some(exif_map);
        let _ = save_primary_metadata(source_path, &metadata);
    }
}

pub fn write_rrexif_sidecar(source_path_str: &str, target_image_path: &Path) -> Result<(), String> {
    let source_path = Path::new(source_path_str);

    let exif_data = if let Some(existing) = read_rrexif_sidecar(source_path) {
        existing
    } else if let Ok(bytes) = fs::read(source_path) {
        read_exif_data_from_bytes(source_path_str, &bytes)
    } else {
        return Ok(());
    };

    if exif_data.is_empty() {
        return Ok(());
    }

    let mut metadata = load_primary_metadata(target_image_path);
    metadata.exif = Some(exif_data);
    save_primary_metadata(target_image_path, &metadata)
        .map_err(|e| format!("Failed to write sidecar: {}", e))
}

#[cfg(test)]
mod tests {
    use super::*;
    use image::{ImageBuffer, Rgb};
    use tempfile::TempDir;

    const MAKER_NOTE: &[u8] = b"FUJIFILM-test-maker-note-blob";

    fn create_jpeg_with_full_exif(path: &Path) {
        let img: ImageBuffer<Rgb<u8>, Vec<u8>> =
            ImageBuffer::from_pixel(64, 64, Rgb([200, 100, 50]));
        img.save(path).unwrap();

        let mut metadata = Metadata::new();
        metadata.set_tag(ExifTag::Make("TestCam".to_string()));
        metadata.set_tag(ExifTag::Model("RapidRAW-Test".to_string()));
        metadata.set_tag(ExifTag::Artist("Original Author".to_string()));
        metadata.set_tag(ExifTag::Copyright("Original Copyright".to_string()));
        metadata.set_tag(ExifTag::Orientation(vec![6u16]));
        metadata.set_tag(ExifTag::Flash(vec![16u16]));
        metadata.set_tag(ExifTag::ApertureValue(vec![uR64 {
            nominator: 13,
            denominator: 1,
        }]));
        metadata.set_tag(ExifTag::OffsetTimeOriginal("+02:00".to_string()));
        metadata.set_tag(ExifTag::SubSecTimeOriginal("00".to_string()));
        metadata.set_tag(ExifTag::SerialNumber("4B035054".to_string()));
        metadata.set_tag(ExifTag::LensSerialNumber("59627836".to_string()));
        metadata.set_tag(ExifTag::MakerNote(MAKER_NOTE.to_vec()));
        metadata.set_tag(ExifTag::GPSLatitudeRef("N".to_string()));
        metadata.set_tag(ExifTag::GPSLatitude(vec![
            uR64 {
                nominator: 53,
                denominator: 1,
            },
            uR64 {
                nominator: 29,
                denominator: 1,
            },
            uR64 {
                nominator: 5299,
                denominator: 100,
            },
        ]));
        metadata.set_tag(ExifTag::GPSLongitudeRef("E".to_string()));
        metadata.set_tag(ExifTag::GPSLongitude(vec![
            uR64 {
                nominator: 7,
                denominator: 1,
            },
            uR64 {
                nominator: 2,
                denominator: 1,
            },
            uR64 {
                nominator: 4427,
                denominator: 100,
            },
        ]));
        metadata.set_tag(ExifTag::GPSAltitude(vec![uR64 {
            nominator: 50,
            denominator: 1,
        }]));
        metadata.set_tag(ExifTag::GPSAltitudeRef(vec![0u8]));

        let mut bytes = fs::read(path).unwrap();
        metadata
            .write_to_vec(&mut bytes, FileExtension::JPEG)
            .unwrap();
        fs::write(path, &bytes).unwrap();
    }

    // Reproduces the bug trigger: opening an image in the app populates the
    // .rrdata sidecar, which made write_image_with_metadata reconstruct the
    // export EXIF from the sidecar's small display-formatted subset.
    fn setup_jpeg_with_sidecar(dir: &TempDir) -> (PathBuf, Vec<u8>) {
        let jpeg_path = dir.path().join("photo.jpg");
        create_jpeg_with_full_exif(&jpeg_path);
        let file_bytes = fs::read(&jpeg_path).unwrap();
        persist_exif_if_missing(&jpeg_path, jpeg_path.to_str().unwrap(), &file_bytes);
        assert!(
            get_primary_sidecar_path(&jpeg_path).exists(),
            ".rrdata sidecar must exist to trigger issue #1165"
        );
        (jpeg_path, file_bytes)
    }

    fn read_export_exif(bytes: &[u8]) -> Exif {
        exif::Reader::new()
            .read_from_container(&mut Cursor::new(bytes))
            .unwrap()
    }

    fn string_field(exif_obj: &Exif, tag: exif::Tag) -> Option<String> {
        let field = exif_obj.get_field(tag, In::PRIMARY)?;
        match &field.value {
            Value::Ascii(vec) => Some(
                vec.iter()
                    .map(|v| String::from_utf8_lossy(v).to_string())
                    .collect::<Vec<String>>()
                    .join(" "),
            ),
            _ => Some(field.display_value().to_string()),
        }
    }

    #[test]
    fn issue_1165_full_exif_preserved_when_sidecar_exists() {
        let dir = TempDir::new().unwrap();
        let (jpeg_path, file_bytes) = setup_jpeg_with_sidecar(&dir);

        let mut export_bytes = file_bytes.clone();
        write_image_with_metadata(
            &mut export_bytes,
            jpeg_path.to_str().unwrap(),
            "jpg",
            true,
            false,
        )
        .unwrap();

        let exif_obj = read_export_exif(&export_bytes);
        for tag in [
            exif::Tag::Make,
            exif::Tag::Model,
            exif::Tag::Artist,
            exif::Tag::Copyright,
            exif::Tag::Flash,
            exif::Tag::ApertureValue,
            exif::Tag::OffsetTimeOriginal,
            exif::Tag::SubSecTimeOriginal,
            exif::Tag::BodySerialNumber,
            exif::Tag::LensSerialNumber,
            exif::Tag::MakerNote,
            exif::Tag::GPSLatitude,
            exif::Tag::GPSLongitude,
            exif::Tag::GPSAltitude,
        ] {
            assert!(
                exif_obj.get_field(tag, In::PRIMARY).is_some(),
                "{} must survive the export (issue #1165)",
                tag
            );
        }

        let maker_note = exif_obj
            .get_field(exif::Tag::MakerNote, In::PRIMARY)
            .unwrap();
        assert!(
            matches!(&maker_note.value, Value::Undefined(bytes, _) if bytes == MAKER_NOTE),
            "MakerNote bytes must be copied unchanged"
        );
    }

    #[test]
    fn issue_1165_gps_stripped_when_strip_gps_true() {
        let dir = TempDir::new().unwrap();
        let (jpeg_path, file_bytes) = setup_jpeg_with_sidecar(&dir);

        let mut export_bytes = file_bytes.clone();
        write_image_with_metadata(
            &mut export_bytes,
            jpeg_path.to_str().unwrap(),
            "jpg",
            true,
            true,
        )
        .unwrap();

        let exif_obj = read_export_exif(&export_bytes);
        for tag in [
            exif::Tag::GPSLatitude,
            exif::Tag::GPSLatitudeRef,
            exif::Tag::GPSLongitude,
            exif::Tag::GPSLongitudeRef,
            exif::Tag::GPSAltitude,
            exif::Tag::GPSAltitudeRef,
        ] {
            assert!(
                exif_obj.get_field(tag, In::PRIMARY).is_none(),
                "{} must be stripped when strip_gps=true",
                tag
            );
        }
        assert!(
            exif_obj.get_field(exif::Tag::Flash, In::PRIMARY).is_some(),
            "non-GPS tags must still be preserved"
        );
    }

    #[test]
    fn sidecar_edits_override_source_values() {
        let dir = TempDir::new().unwrap();
        let (jpeg_path, file_bytes) = setup_jpeg_with_sidecar(&dir);

        // Simulate edits in the metadata panel: Artist gets a new value,
        // Copyright is cleared (update_exif_fields removes the key).
        let mut sidecar = load_primary_metadata(&jpeg_path);
        let mut exif_map = sidecar.exif.unwrap();
        exif_map.insert("Artist".to_string(), "Edited Author".to_string());
        exif_map.remove("Copyright");
        // Marker that truncate_large_exif leaves for oversized values; must
        // not be mistaken for a user edit.
        exif_map.insert("ImageDescription".to_string(), "\"   ...   \"".to_string());
        sidecar.exif = Some(exif_map);
        save_primary_metadata(&jpeg_path, &sidecar).unwrap();

        let mut export_bytes = file_bytes.clone();
        write_image_with_metadata(
            &mut export_bytes,
            jpeg_path.to_str().unwrap(),
            "jpg",
            true,
            false,
        )
        .unwrap();

        let exif_obj = read_export_exif(&export_bytes);
        assert_eq!(
            string_field(&exif_obj, exif::Tag::Artist).as_deref(),
            Some("Edited Author"),
            "sidecar edits must override the source value"
        );
        assert!(
            exif_obj
                .get_field(exif::Tag::Copyright, In::PRIMARY)
                .is_none(),
            "cleared fields must not reappear from the source file"
        );
        assert!(
            exif_obj.get_field(exif::Tag::Flash, In::PRIMARY).is_some(),
            "unedited tags must still come from the source file"
        );
        assert!(
            exif_obj
                .get_field(exif::Tag::ImageDescription, In::PRIMARY)
                .is_none(),
            "truncation artifacts in the sidecar must not become tags"
        );
    }

    #[test]
    fn orientation_reset_and_dimension_tags_updated() {
        let dir = TempDir::new().unwrap();
        let (jpeg_path, _) = setup_jpeg_with_sidecar(&dir);

        // The export pipeline bakes the rotation into the pixels, so the
        // export of the 64x64 source is 32x64 here to make stale dimension
        // tags detectable.
        let rotated: ImageBuffer<Rgb<u8>, Vec<u8>> =
            ImageBuffer::from_pixel(32, 64, Rgb([200, 100, 50]));
        let mut export_bytes = Vec::new();
        rotated
            .write_to(
                &mut Cursor::new(&mut export_bytes),
                image::ImageFormat::Jpeg,
            )
            .unwrap();

        write_image_with_metadata(
            &mut export_bytes,
            jpeg_path.to_str().unwrap(),
            "jpg",
            true,
            false,
        )
        .unwrap();

        let exif_obj = read_export_exif(&export_bytes);
        let orientation = exif_obj
            .get_field(exif::Tag::Orientation, In::PRIMARY)
            .and_then(|f| f.value.get_uint(0));
        assert_eq!(
            orientation,
            Some(1),
            "rotation is baked into the pixels, so Orientation must be reset"
        );
        let width = exif_obj
            .get_field(exif::Tag::PixelXDimension, In::PRIMARY)
            .and_then(|f| f.value.get_uint(0));
        let height = exif_obj
            .get_field(exif::Tag::PixelYDimension, In::PRIMARY)
            .and_then(|f| f.value.get_uint(0));
        assert_eq!(
            (width, height),
            (Some(32), Some(64)),
            "dimension tags must match the exported pixels"
        );
    }

    #[test]
    fn issue_1322_webp_export_carries_exif() {
        let dir = TempDir::new().unwrap();
        let (jpeg_path, _) = setup_jpeg_with_sidecar(&dir);

        let img: ImageBuffer<Rgb<u8>, Vec<u8>> =
            ImageBuffer::from_pixel(64, 64, Rgb([200, 100, 50]));
        let mut lossless_bytes = Vec::new();
        img.write_to(
            &mut Cursor::new(&mut lossless_bytes),
            image::ImageFormat::WebP,
        )
        .unwrap();
        // Same encoder the export pipeline uses (lossy VP8).
        let lossy_bytes = webp::Encoder::from_image(&image::DynamicImage::ImageRgb8(img))
            .unwrap()
            .encode(80.0)
            .to_vec();

        for mut export_bytes in [lossless_bytes, lossy_bytes] {
            write_image_with_metadata(
                &mut export_bytes,
                jpeg_path.to_str().unwrap(),
                "webp",
                true,
                false,
            )
            .unwrap();

            let exif_obj = read_export_exif(&export_bytes);
            for tag in [
                exif::Tag::Make,
                exif::Tag::Flash,
                exif::Tag::MakerNote,
                exif::Tag::GPSLatitude,
            ] {
                assert!(
                    exif_obj.get_field(tag, In::PRIMARY).is_some(),
                    "{} must be written to the WebP EXIF chunk (issue #1322)",
                    tag
                );
            }
        }
    }
}
