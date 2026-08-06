import json
from pathlib import Path

LOCALES_DIR = Path("./locales")

TRANSLATIONS = {
    "ca": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "Plegar el panell esquerre",
                    "expandLeft": "Desplegar el panell esquerre",
                    "collapseRight": "Plegar el panell dret",
                    "expandRight": "Desplegar el panell dret"
                }
            }
        }
    },
    "de": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "Linkes Panel einklappen",
                    "expandLeft": "Linkes Panel ausklappen",
                    "collapseRight": "Rechtes Panel einklappen",
                    "expandRight": "Rechtes Panel ausklappen"
                }
            }
        }
    },
    "en": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "Collapse Left Panel",
                    "expandLeft": "Expand Left Panel",
                    "collapseRight": "Collapse Right Panel",
                    "expandRight": "Expand Right Panel"
                }
            }
        }
    },
    "es": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "Contraer panel izquierdo",
                    "expandLeft": "Expandir panel izquierdo",
                    "collapseRight": "Contraer panel derecho",
                    "expandRight": "Expandir panel derecho"
                }
            }
        }
    },
    "fr": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "Réduire le panneau gauche",
                    "expandLeft": "Agrandir le panneau gauche",
                    "collapseRight": "Réduire le panneau droit",
                    "expandRight": "Agrandir le panneau droit"
                }
            }
        }
    },
    "it": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "Riduci pannello sinistro",
                    "expandLeft": "Espandi pannello sinistro",
                    "collapseRight": "Riduci pannello destro",
                    "expandRight": "Espandi pannello destro"
                }
            }
        }
    },
    "ja": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "左パネルを折りたたむ",
                    "expandLeft": "左パネルを展開",
                    "collapseRight": "右パネルを折りたたむ",
                    "expandRight": "右パネルを展開"
                }
            }
        }
    },
    "ko": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "왼쪽 패널 접기",
                    "expandLeft": "왼쪽 패널 펼치기",
                    "collapseRight": "오른쪽 패널 접기",
                    "expandRight": "오른쪽 패널 펼치기"
                }
            }
        }
    },
    "pl": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "Zwiń lewy panel",
                    "expandLeft": "Rozwiń lewy panel",
                    "collapseRight": "Zwiń prawy panel",
                    "expandRight": "Rozwiń prawy panel"
                }
            }
        }
    },
    "pt": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "Recolher painel esquerdo",
                    "expandLeft": "Expandir painel esquerdo",
                    "collapseRight": "Recolher painel direito",
                    "expandRight": "Expandir painel direito"
                }
            }
        }
    },
    "ru": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "Свернуть левую панель",
                    "expandLeft": "Развернуть левую панель",
                    "collapseRight": "Свернуть правую панель",
                    "expandRight": "Развернуть правую панель"
                }
            }
        }
    },
    "zh-CN": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "折叠左侧面板",
                    "expandLeft": "展开左侧面板",
                    "collapseRight": "折叠右侧面板",
                    "expandRight": "展开右侧面板"
                }
            }
        }
    },
    "zh-TW": {
        "ui": {
            "bottomBar": {
                "tooltips": {
                    "collapseLeft": "折疊左側面板",
                    "expandLeft": "展開左側面板",
                    "collapseRight": "折疊右側面板",
                    "expandRight": "展開右側面板"
                }
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

    deep_merge(data, trans)
    sorted_data = sort_dict_recursively(data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Updated and Sorted: {file_path.name}")

def main():
    if not LOCALES_DIR.exists():
        print(f"Error: Locales directory '{LOCALES_DIR}' does not exist.")
        return

    print("Starting Panel Tooltip translation updates...")
    for lang, trans in TRANSLATIONS.items():
        file_path = LOCALES_DIR / f"{lang}.json"
        update_json_file(file_path, trans)
    print("Done!")

if __name__ == "__main__":
    main()
