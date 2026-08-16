#![allow(unused_variables)]

use std::collections::HashMap;
use serde::Serialize;
#[cfg(feature = "tethering")]
use tauri::Manager;
#[cfg(feature = "tethering")]
use crate::AppState;

#[derive(Serialize)]
pub struct CameraConfigChoice {
    pub name: String,
    pub current_value: String,
    pub choices: Vec<String>,
}

#[cfg(feature = "tethering")]
pub struct CameraSession {
    pub context: Option<gphoto2::Context>,
    pub camera: Option<gphoto2::Camera>,
}

#[cfg(not(feature = "tethering"))]
pub struct CameraSession {}

impl CameraSession {
    pub fn new() -> Self {
        #[cfg(feature = "tethering")]
        {
            Self {
                context: gphoto2::Context::new().ok(),
                camera: None,
            }
        }
        #[cfg(not(feature = "tethering"))]
        {
            Self {}
        }
    }
}

unsafe impl Send for CameraSession {}
unsafe impl Sync for CameraSession {}

#[tauri::command]
pub async fn tether_list_cameras(app_handle: tauri::AppHandle) -> Result<Vec<String>, String> {
    #[cfg(feature = "tethering")]
    {
        tauri::async_runtime::spawn_blocking(move || {
            let state = app_handle.state::<AppState>();
            let mut session = state.camera_session.lock().unwrap();
            
            if session.context.is_none() {
                session.context = gphoto2::Context::new().ok();
            }
            
            let context = session.context.as_ref().ok_or("Failed to initialize gphoto2 context")?;
            let cameras = gphoto2::Camera::autodetect(context).map_err(|e| e.to_string())?;
            Ok(cameras.into_iter().map(|c| format!("{} ({})", c.model, c.port)).collect())
        })
        .await
        .map_err(|e| format!("Task panicked: {}", e))?
    }
    #[cfg(not(feature = "tethering"))]
    Err("Tethering is not supported in this build.".into())
}

#[tauri::command]
pub async fn tether_connect(app_handle: tauri::AppHandle) -> Result<String, String> {
    #[cfg(feature = "tethering")]
    {
        tauri::async_runtime::spawn_blocking(move || {
            let state = app_handle.state::<AppState>();
            let mut session = state.camera_session.lock().unwrap();

            session.camera = None;
            std::thread::sleep(std::time::Duration::from_millis(150));

            if session.context.is_none() {
                session.context = gphoto2::Context::new().ok();
            }
            let context = session.context.as_ref().ok_or("Failed to initialize gphoto2 context")?;
            
            let cameras = gphoto2::Camera::autodetect(context).map_err(|e| e.to_string())?;
            let descriptor = cameras.into_iter().next().ok_or("No camera found")?;

            let camera = match gphoto2::Camera::open(context, &descriptor.model, &descriptor.port) {
                Ok(cam) => cam,
                Err(_) => {
                    std::thread::sleep(std::time::Duration::from_millis(300));
                    gphoto2::Camera::open(context, &descriptor.model, &descriptor.port)
                        .map_err(|e| format!("Failed to connect to camera: {}", e))?
                }
            };

            if let Ok(widget) = camera.get_single_config(context, "capturetarget") {
                let choices = widget.choices().unwrap_or_default();
                if let Some(ram_choice) = choices.iter().find(|c| c.to_lowercase().contains("ram") || c.to_lowercase().contains("sdram")) {
                    let _ = widget.set_choice(ram_choice);
                    let _ = camera.set_single_config(context, "capturetarget", &widget);
                }
            }

            if let Ok(widget) = camera.get_single_config(context, "drivemode") {
                let choices = widget.choices().unwrap_or_default();
                if let Some(single_choice) = choices.iter().find(|c| c.to_lowercase().contains("single")) {
                    let _ = widget.set_choice(single_choice);
                    let _ = camera.set_single_config(context, "drivemode", &widget);
                }
            }

            let _ = camera.capture_preview(context);

            for _ in 0..15 {
                if let Ok(event) = camera.wait_for_event(context, std::time::Duration::from_millis(30)) {
                    if let gphoto2::CameraEvent::Timeout = event {
                        break;
                    }
                }
            }

            let model_name = descriptor.model.clone();
            session.camera = Some(camera);
            
            Ok(format!("Connected to {}", model_name))
        })
        .await
        .map_err(|e| format!("Task panicked: {}", e))?
    }
    #[cfg(not(feature = "tethering"))]
    Err("Tethering is not supported in this build.".into())
}

#[tauri::command]
pub async fn tether_get_settings(app_handle: tauri::AppHandle) -> Result<HashMap<String, CameraConfigChoice>, String> {
    #[cfg(feature = "tethering")]
    {
        tauri::async_runtime::spawn_blocking(move || {
            use gphoto2::widget::WidgetValue;

            let state = app_handle.state::<AppState>();
            let session = state.camera_session.lock().unwrap();
            let camera = session.camera.as_ref().ok_or("No camera connected")?;
            let context = session.context.as_ref().ok_or("No context initialized")?;

            let keys_to_query: [(&str, &[&str]); 4] = [
                ("iso", &["iso", "iso-speed", "ISO"]),
                ("shutterspeed", &["shutterspeed", "exposure-time", "exposurespeed"]),
                ("aperture", &["f-number", "aperture", "fnumber"]),
                ("whitebalance", &["whitebalance", "white-balance"]),
            ];

            let mut attempts = 0;
            let mut map = HashMap::new();

            while attempts < 3 {
                map.clear();
                for (frontend_key, aliases) in keys_to_query.iter() {
                    for &camera_key in *aliases {
                        if let Ok(widget) = camera.get_single_config(context, camera_key) {
                            let current_value = match widget.value() {
                                Ok(WidgetValue::Choice(s)) => s,
                                Ok(WidgetValue::Text(s)) => s,
                                Ok(WidgetValue::Range(f)) => f.to_string(),
                                _ => continue,
                            };

                            let choices = widget.choices().unwrap_or_default();

                            map.insert(
                                frontend_key.to_string(),
                                CameraConfigChoice {
                                    name: frontend_key.to_string(),
                                    current_value,
                                    choices,
                                },
                            );
                            break;
                        }
                    }
                }

                let has_glitched_values = map.values().any(|cfg| {
                    cfg.current_value.contains("65535") 
                    || cfg.current_value.contains("Unknown value 0000")
                });

                if !has_glitched_values && !map.is_empty() {
                    break;
                }

                attempts += 1;
                let _ = camera.wait_for_event(context, std::time::Duration::from_millis(200));
            }

            Ok(map)
        })
        .await
        .map_err(|e| format!("Task panicked: {}", e))?
    }
    #[cfg(not(feature = "tethering"))]
    Err("Tethering is not supported in this build.".into())
}

#[tauri::command]
pub async fn tether_set_setting(
    app_handle: tauri::AppHandle,
    setting_name: String,
    value: String,
) -> Result<(), String> {
    #[cfg(feature = "tethering")]
    {
        tauri::async_runtime::spawn_blocking(move || {
            use gphoto2::widget::WidgetType;

            let state = app_handle.state::<AppState>();
            let session = state.camera_session.lock().unwrap();
            let camera = session.camera.as_ref().ok_or("No camera connected")?; 
            let context = session.context.as_ref().ok_or("No context initialized")?;

            let aliases: &[&str] = match setting_name.as_str() {
                "iso" => &["iso", "iso-speed", "ISO"],
                "shutterspeed" => &["shutterspeed", "exposure-time", "exposurespeed"],
                "aperture" => &["f-number", "aperture", "fnumber"],
                "whitebalance" => &["whitebalance", "white-balance"],
                _ => &[],
            };

            let mut applied = false;
            for &camera_key in aliases {
                if let Ok(widget) = camera.get_single_config(context, camera_key) {
                    if let Ok(widget_type) = widget.widget_type() {
                        let set_ok = match widget_type {
                            WidgetType::Radio | WidgetType::Menu => widget.set_choice(&value).is_ok(),
                            WidgetType::Text => widget.set_text(&value).is_ok(),
                            _ => false,
                        };

                        if set_ok && camera.set_single_config(context, camera_key, &widget).is_ok() {
                            applied = true;
                            break;
                        }
                    }
                }
            }

            if !applied {
                return Err(format!("Failed to set {} to {}", setting_name, value));
            }

            Ok(())
        })
        .await
        .map_err(|e| format!("Task panicked: {}", e))?
    }
    #[cfg(not(feature = "tethering"))]
    Err("Tethering is not supported in this build.".into())
}

#[tauri::command]
pub async fn tether_get_preview(app_handle: tauri::AppHandle) -> Result<Vec<u8>, String> {
    #[cfg(feature = "tethering")]
    {
        tauri::async_runtime::spawn_blocking(move || {
            let state = app_handle.state::<AppState>();
            let session = state.camera_session.lock().unwrap();
            let camera = session.camera.as_ref().ok_or("No camera connected")?;
            let context = session.context.as_ref().ok_or("No context initialized")?;

            let file = camera.capture_preview(context)
                .map_err(|e| format!("Failed to capture preview: {}", e))?;

            let data = file.data().map_err(|e| e.to_string())?;
            
            Ok(data.to_vec())
        })
        .await
        .map_err(|e| format!("Task panicked: {}", e))?
    }
    #[cfg(not(feature = "tethering"))]
    Err("Tethering is not supported in this build.".into())
}

#[tauri::command]
pub async fn tether_capture(
    app_handle: tauri::AppHandle,
    destination_folder: Option<String>,
) -> Result<String, String> {
    #[cfg(feature = "tethering")]
    {
        tauri::async_runtime::spawn_blocking(move || {
            let state = app_handle.state::<AppState>();
            let session = state.camera_session.lock().unwrap();
            let camera = session.camera.as_ref().ok_or("No camera connected")?;
            let context = session.context.as_ref().ok_or("No context initialized")?;
            
            while let Ok(event) = camera.wait_for_event(context, std::time::Duration::from_millis(10)) {
                if let gphoto2::CameraEvent::Timeout = event {
                    break;
                }
            }

            let camera_file_path = camera.capture_image(context)
                .map_err(|e| format!("Capture failed: {}", e))?;
            
            let file = camera.download(context, &camera_file_path)
                .map_err(|e| format!("Download failed: {}", e))?;
            
            let save_dir = destination_folder.unwrap_or_else(|| std::env::temp_dir().to_string_lossy().to_string());
            let output_path = std::path::Path::new(&save_dir).join(&camera_file_path.name);
            
            std::fs::write(&output_path, file.data().map_err(|e| e.to_string())?)
                .map_err(|e| format!("Failed to save captured file: {}", e))?;
                
            let _ = camera.delete_file(context, &camera_file_path.folder, &camera_file_path.name);

            Ok(output_path.to_string_lossy().to_string())
        })
        .await
        .map_err(|e| format!("Task panicked: {}", e))?
    }
    #[cfg(not(feature = "tethering"))]
    Err("Tethering is not supported in this build.".into())
}
