import json
from pathlib import Path

LOCALES_DIR = Path("./locales")

TRANSLATIONS = {
    "ca": {
        "editor": {
            "guided": {
                "drawingActive": "Dibuix actiu"
            }
        },
        "modals": {
            "transform": {
                "geometry": "Geometria"
            }
        }
    },
    "de": {
        "editor": {
            "guided": {
                "drawingActive": "Zeichnen aktiv"
            }
        },
        "modals": {
            "transform": {
                "geometry": "Geometrie"
            }
        }
    },
    "en": {
        "editor": {
            "guided": {
                "drawingActive": "Drawing Active"
            }
        },
        "modals": {
            "transform": {
                "geometry": "Geometry"
            }
        }
    },
    "es": {
        "editor": {
            "guided": {
                "drawingActive": "Dibujo activo"
            }
        },
        "modals": {
            "transform": {
                "geometry": "Geometría"
            }
        }
    },
    "fr": {
        "editor": {
            "guided": {
                "drawingActive": "Dessin actif"
            }
        },
        "modals": {
            "transform": {
                "geometry": "Géométrie"
            }
        }
    },
    "it": {
        "editor": {
            "guided": {
                "drawingActive": "Disegno attivo"
            }
        },
        "modals": {
            "transform": {
                "geometry": "Geometria"
            }
        }
    },
    "ja": {
        "editor": {
            "guided": {
                "drawingActive": "描画中"
            }
        },
        "modals": {
            "transform": {
                "geometry": "ジオメトリ"
            }
        }
    },
    "ko": {
        "editor": {
            "guided": {
                "drawingActive": "그리기 활성화"
            }
        },
        "modals": {
            "transform": {
                "geometry": "기하학"
            }
        }
    },
    "pl": {
        "editor": {
            "guided": {
                "drawingActive": "Rysowanie aktywne"
            }
        },
        "modals": {
            "transform": {
                "geometry": "Geometria"
            }
        }
    },
    "pt": {
        "editor": {
            "guided": {
                "drawingActive": "Desenho ativo"
            }
        },
        "modals": {
            "transform": {
                "geometry": "Geometria"
            }
        }
    },
    "ru": {
        "editor": {
            "guided": {
                "drawingActive": "Рисование активно"
            }
        },
        "modals": {
            "transform": {
                "geometry": "Геометрия"
            }
        }
    },
    "zh-CN": {
        "editor": {
            "guided": {
                "drawingActive": "绘图中"
            }
        },
        "modals": {
            "transform": {
                "geometry": "几何"
            }
        }
    },
    "zh-TW": {
        "editor": {
            "guided": {
                "drawingActive": "繪圖中"
            }
        },
        "modals": {
            "transform": {
                "geometry": "幾何"
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

    print("Starting translation updates for drawingActive and geometry...")
    for lang, trans in TRANSLATIONS.items():
        file_path = LOCALES_DIR / f"{lang}.json"
        update_json_file(file_path, trans)
    print("Done!")

if __name__ == "__main__":
    main()
