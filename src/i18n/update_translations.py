import json
from pathlib import Path

LOCALES_DIR = Path("./locales")

TRANSLATIONS = {
    "ca": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "Retoc {{count}}"
                },
                "touchUpTitle": "Retocs"
            }
        },
        "masks": {
            "types": {
                "retouch": "Retoc"
            }
        }
    },
    "de": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "Retusche {{count}}"
                },
                "touchUpTitle": "Ausbessern"
            }
        },
        "masks": {
            "types": {
                "retouch": "Retuschieren"
            }
        }
    },
    "en": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "Retouch {{count}}"
                },
                "touchUpTitle": "Touch Up"
            }
        },
        "masks": {
            "types": {
                "retouch": "Retouch"
            }
        }
    },
    "es": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "Retoque {{count}}"
                },
                "touchUpTitle": "Retoques"
            }
        },
        "masks": {
            "types": {
                "retouch": "Retocar"
            }
        }
    },
    "fr": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "Retouche {{count}}"
                },
                "touchUpTitle": "Retouches"
            }
        },
        "masks": {
            "types": {
                "retouch": "Retouche"
            }
        }
    },
    "it": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "Ritocco {{count}}"
                },
                "touchUpTitle": "Ritocchi"
            }
        },
        "masks": {
            "types": {
                "retouch": "Ritocco"
            }
        }
    },
    "ja": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "レタッチ {{count}}"
                },
                "touchUpTitle": "タッチアップ"
            }
        },
        "masks": {
            "types": {
                "retouch": "レタッチ"
            }
        }
    },
    "ko": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "리터칭 {{count}}"
                },
                "touchUpTitle": "터치업"
            }
        },
        "masks": {
            "types": {
                "retouch": "리터칭"
            }
        }
    },
    "pl": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "Retusz {{count}}"
                },
                "touchUpTitle": "Poprawki"
            }
        },
        "masks": {
            "types": {
                "retouch": "Retusz"
            }
        }
    },
    "pt": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "Retoque {{count}}"
                },
                "touchUpTitle": "Retoques"
            }
        },
        "masks": {
            "types": {
                "retouch": "Retoque"
            }
        }
    },
    "ru": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "Ретушь {{count}}"
                },
                "touchUpTitle": "Ретушь"
            }
        },
        "masks": {
            "types": {
                "retouch": "Ретушь"
            }
        }
    },
    "zh-CN": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "修饰 {{count}}"
                },
                "touchUpTitle": "润色"
            }
        },
        "masks": {
            "types": {
                "retouch": "修饰"
            }
        }
    },
    "zh-TW": {
        "editor": {
            "ai": {
                "patches": {
                    "retouch": "修飾 {{count}}"
                },
                "touchUpTitle": "潤色"
            }
        },
        "masks": {
            "types": {
                "retouch": "修飾"
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

    print("Starting translation updates for Retouch strings...")
    for lang, trans in TRANSLATIONS.items():
        file_path = LOCALES_DIR / f"{lang}.json"
        update_json_file(file_path, trans)
    print("Done!")

if __name__ == "__main__":
    main()
