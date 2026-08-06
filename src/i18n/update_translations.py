import json
from pathlib import Path

LOCALES_DIR = Path("./locales")

TRANSLATIONS = {
    "ca": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "Commutar el panell esquerre",
                    "toggle_right_panel": "Commutar el panell dret",
                    "toggle_bottom_panel": "Commutar la tira d'imatges"
                }
            }
        }
    },
    "de": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "Linkes Panel ein-/ausblenden",
                    "toggle_right_panel": "Rechtes Panel ein-/ausblenden",
                    "toggle_bottom_panel": "Filmstreifen ein-/ausblenden"
                }
            }
        }
    },
    "en": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "Toggle Left Panel",
                    "toggle_right_panel": "Toggle Right Panel",
                    "toggle_bottom_panel": "Toggle Filmstrip"
                }
            }
        }
    },
    "es": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "Alternar panel izquierdo",
                    "toggle_right_panel": "Alternar panel derecho",
                    "toggle_bottom_panel": "Alternar tira de imágenes"
                }
            }
        }
    },
    "fr": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "Afficher/Masquer le panneau gauche",
                    "toggle_right_panel": "Afficher/Masquer le panneau droit",
                    "toggle_bottom_panel": "Afficher/Masquer la bande de film"
                }
            }
        }
    },
    "it": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "Mostra/Nascondi pannello sinistro",
                    "toggle_right_panel": "Mostra/Nascondi pannello destro",
                    "toggle_bottom_panel": "Mostra/Nascondi striscia immagini"
                }
            }
        }
    },
    "ja": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "左パネルの表示/非表示",
                    "toggle_right_panel": "右パネルの表示/非表示",
                    "toggle_bottom_panel": "フィルムストリップの表示/非表示"
                }
            }
        }
    },
    "ko": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "왼쪽 패널 토글",
                    "toggle_right_panel": "오른쪽 패널 토글",
                    "toggle_bottom_panel": "필름스트립 토글"
                }
            }
        }
    },
    "pl": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "Przełącz lewy panel",
                    "toggle_right_panel": "Przełącz prawy panel",
                    "toggle_bottom_panel": "Przełącz pasek z klatkami"
                }
            }
        }
    },
    "pt": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "Alternar painel esquerdo",
                    "toggle_right_panel": "Alternar painel direito",
                    "toggle_bottom_panel": "Alternar tira de filme"
                }
            }
        }
    },
    "ru": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "Показать/скрыть левую панель",
                    "toggle_right_panel": "Показать/скрыть правую панель",
                    "toggle_bottom_panel": "Показать/скрыть ленту кадров"
                }
            }
        }
    },
    "zh-CN": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "切换左侧面板",
                    "toggle_right_panel": "切换右侧面板",
                    "toggle_bottom_panel": "切换胶片条"
                }
            }
        }
    },
    "zh-TW": {
        "settings": {
            "keybinds": {
                "actions": {
                    "toggle_left_panel": "切換左側面板",
                    "toggle_right_panel": "切換右側面板",
                    "toggle_bottom_panel": "切換膠片條"
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

    print("Starting Keybind translation updates...")
    for lang, trans in TRANSLATIONS.items():
        file_path = LOCALES_DIR / f"{lang}.json"
        update_json_file(file_path, trans)
    print("Done!")

if __name__ == "__main__":
    main()
