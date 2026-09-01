import json
from pathlib import Path

LOCALES_DIR = Path("./locales")

TRANSLATIONS = {
    "ca": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "Correcció d'objectiu automàtica"
            },
            "thumbnail": {
                "autoLensCorrection_one": "Correcció d'objectiu automàtica",
                "autoLensCorrection_other": "Correcció d'objectiu automàtica"
            }
        }
    },
    "de": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "Autom. Objektivkorrektur"
            },
            "thumbnail": {
                "autoLensCorrection_one": "Autom. Objektivkorrektur",
                "autoLensCorrection_other": "Autom. Objektivkorrektur"
            }
        }
    },
    "en": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "Auto Lens Correction"
            },
            "thumbnail": {
                "autoLensCorrection_one": "Auto Lens Correction",
                "autoLensCorrection_other": "Auto Lens Correction"
            }
        }
    },
    "es": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "Corrección de lente automática"
            },
            "thumbnail": {
                "autoLensCorrection_one": "Corrección de lente automática",
                "autoLensCorrection_other": "Corrección de lente automática"
            }
        }
    },
    "fr": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "Correction d'objectif automatique"
            },
            "thumbnail": {
                "autoLensCorrection_one": "Correction d'objectif automatique",
                "autoLensCorrection_other": "Corrections d'objectif automatiques"
            }
        }
    },
    "it": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "Correzione automatica obiettivo"
            },
            "thumbnail": {
                "autoLensCorrection_one": "Correzione automatica obiettivo",
                "autoLensCorrection_other": "Correzione automatica obiettivo"
            }
        }
    },
    "ja": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "自動レンズ補正"
            },
            "thumbnail": {
                "autoLensCorrection_one": "自動レンズ補正",
                "autoLensCorrection_other": "自動レンズ補正"
            }
        }
    },
    "ko": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "자동 렌즈 교정"
            },
            "thumbnail": {
                "autoLensCorrection_one": "자동 렌즈 교정",
                "autoLensCorrection_other": "자동 렌즈 교정"
            }
        }
    },
    "pl": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "Automatyczna korekcja obiektywu"
            },
            "thumbnail": {
                "autoLensCorrection_one": "Automatyczna korekcja obiektywu",
                "autoLensCorrection_other": "Automatyczna korekcja obiektywu"
            }
        }
    },
    "pt": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "Correção automática de lente"
            },
            "thumbnail": {
                "autoLensCorrection_one": "Correção automática de lente",
                "autoLensCorrection_other": "Correção automática de lente"
            }
        }
    },
    "ru": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "Автокоррекция объектива"
            },
            "thumbnail": {
                "autoLensCorrection_one": "Автокоррекция объектива",
                "autoLensCorrection_other": "Автокоррекция объектива"
            }
        }
    },
    "zh-CN": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "自动镜头校正"
            },
            "thumbnail": {
                "autoLensCorrection_one": "自动镜头校正",
                "autoLensCorrection_other": "自动镜头校正"
            }
        }
    },
    "zh-TW": {
        "contextMenus": {
            "editor": {
                "autoLensCorrection": "自動鏡頭校正"
            },
            "thumbnail": {
                "autoLensCorrection_one": "自動鏡頭校正",
                "autoLensCorrection_other": "自動鏡頭校正"
            }
        }
    }
}

def deep_merge(target: dict, source: dict):
    """Recursively merges source dict into target dict."""
    for key, value in source.items():
        if isinstance(value, dict):
            node = target.setdefault(key, {})
            if isinstance(node, dict):
                deep_merge(node, value)
        else:
            target[key] = value

def sort_dict_recursively(item):
    if isinstance(item, dict):
        return {k: sort_dict_recursively(v) for k, v in sorted(item.items())}
    elif isinstance(item, list):
        return [sort_dict_recursively(x) for x in item]
    return item

def update_json_file(file_path: Path, trans: dict):
    if not file_path.exists():
        print(f"Skipping: {file_path.name} (File not found)")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error parsing JSON in {file_path.name}. Skipping.")
        return

    # 1. Merge new translations
    deep_merge(data, trans)

    # 2. Sort alphabetically to maintain formatting consistency
    sorted_data = sort_dict_recursively(data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Updated and Sorted: {file_path.name}")

def main():
    if not LOCALES_DIR.exists():
        print(f"Error: Locales directory '{LOCALES_DIR}' does not exist.")
        return

    print("Starting translation updates for Auto Lens Correction...")
    for lang, trans in TRANSLATIONS.items():
        file_path = LOCALES_DIR / f"{lang}.json"
        update_json_file(file_path, trans)
    print("Done!")

if __name__ == "__main__":
    main()
