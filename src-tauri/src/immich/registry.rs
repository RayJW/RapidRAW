use once_cell::sync::Lazy;
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::sync::RwLock;

#[derive(Debug, Clone)]
pub struct RemoteImage {
    pub asset_id: String,
    pub listed_asset_id: String,
    pub album_id: Option<String>,
}

static ENTRIES: Lazy<RwLock<HashMap<PathBuf, RemoteImage>>> =
    Lazy::new(|| RwLock::new(HashMap::new()));

pub fn insert(path: PathBuf, image: RemoteImage) {
    ENTRIES.write().unwrap().insert(path, image);
}

pub fn get(path: &Path) -> Option<RemoteImage> {
    ENTRIES.read().unwrap().get(path).cloned()
}

pub fn set_listed_asset(path: &Path, listed_asset_id: &str) {
    if let Some(entry) = ENTRIES.write().unwrap().get_mut(path) {
        entry.listed_asset_id = listed_asset_id.to_string();
    }
}

pub fn is_placeholder(path: &Path) -> bool {
    let known = ENTRIES
        .read()
        .map(|entries| entries.contains_key(path))
        .unwrap_or(false);
    known && !path.exists()
}

pub fn clear() {
    ENTRIES.write().unwrap().clear();
}
