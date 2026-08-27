import json
from pathlib import Path

LOCALES_DIR = Path("./locales")

TRANSLATIONS = {
    "ca": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "Resolució de les miniatures de la quadrícula",
                "smallThumbnailResDesc": "Resolució de les miniatures que es mostren a la quadrícula de la biblioteca.",
                "mediumThumbnailRes": "Resolució de la miniatura de l'editor",
                "mediumThumbnailResDesc": "Resolució de la previsualització que es mostra mentre les imatges completes es carreguen a l'editor."
            }
        }
    },
    "de": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "Raster-Miniaturbild-Auflösung",
                "smallThumbnailResDesc": "Auflösung der Miniaturbilder, die im Bibliotheksraster angezeigt werden.",
                "mediumThumbnailRes": "Editor-Miniaturbild-Auflösung",
                "mediumThumbnailResDesc": "Auflösung der Vorschau, die während des Ladens von vollständigen Bildern im Editor angezeigt wird."
            }
        }
    },
    "en": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "Grid Thumbnail Resolution",
                "smallThumbnailResDesc": "Resolution of thumbnails shown in the library grid.",
                "mediumThumbnailRes": "Editor Thumbnail Resolution",
                "mediumThumbnailResDesc": "Resolution of the preview shown while full images load in the editor."
            }
        }
    },
    "es": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "Resolución de miniaturas de la cuadrícula",
                "smallThumbnailResDesc": "Resolución de las miniaturas mostradas en la cuadrícula de la biblioteca.",
                "mediumThumbnailRes": "Resolución de miniaturas del editor",
                "mediumThumbnailResDesc": "Resolución de la vista previa mostrada mientras se cargan imágenes completas en el editor."
            }
        }
    },
    "fr": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "Résolution des vignettes de la grille",
                "smallThumbnailResDesc": "Résolution des vignettes affichées dans la grille de la bibliothèque.",
                "mediumThumbnailRes": "Résolution des vignettes de l'éditeur",
                "mediumThumbnailResDesc": "Résolution de l'aperçu affiché pendant le chargement complet des images dans l'éditeur."
            }
        }
    },
    "it": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "Risoluzione delle miniature della griglia",
                "smallThumbnailResDesc": "Risoluzione delle miniature mostrate nella griglia della libreria.",
                "mediumThumbnailRes": "Risoluzione della miniatura dell'editor",
                "mediumThumbnailResDesc": "Risoluzione dell'anteprima mostrata mentre le immagini complete vengono caricate nell'editor."
            }
        }
    },
    "ja": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "グリッドサムネイルの解像度",
                "smallThumbnailResDesc": "ライブラリのグリッドに表示されるサムネイルの解像度。",
                "mediumThumbnailRes": "エディターサムネイルの解像度",
                "mediumThumbnailResDesc": "完全な画像がエディターに読み込まれる間に表示されるプレビューの解像度。"
            }
        }
    },
    "ko": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "그리드 썸네일 해상도",
                "smallThumbnailResDesc": "라이브러리 그리드에 표시되는 썸네일의 해상도입니다.",
                "mediumThumbnailRes": "편집기 썸네일 해상도",
                "mediumThumbnailResDesc": "전체 이미지가 편집기에 로드되는 동안 표시되는 미리보기의 해상도입니다."
            }
        }
    },
    "pl": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "Rozdzielczość miniatur w siatce",
                "smallThumbnailResDesc": "Rozdzielczość miniatur wyświetlanych w siatce biblioteki.",
                "mediumThumbnailRes": "Rozdzielczość miniatury edytora",
                "mediumThumbnailResDesc": "Rozdzielczość podglądu wyświetlanego podczas ładowania pełnych obrazów w edytorze."
            }
        }
    },
    "pt": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "Resolução das miniaturas da grade",
                "smallThumbnailResDesc": "Resolução das miniaturas exibidas na grade da biblioteca.",
                "mediumThumbnailRes": "Resolução da miniatura do editor",
                "mediumThumbnailResDesc": "Resolução da visualização exibida enquanto as imagens completas carregam no editor."
            }
        }
    },
    "ru": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "Разрешение миниатюр в сетке",
                "smallThumbnailResDesc": "Разрешение миниатюр, отображаемых в сетке библиотеки.",
                "mediumThumbnailRes": "Разрешение миниатюр в редакторе",
                "mediumThumbnailResDesc": "Разрешение превью, отображаемого при загрузке полных изображений в редакторе."
            }
        }
    },
    "zh-CN": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "网格缩略图分辨率",
                "smallThumbnailResDesc": "图库网格中显示的缩略图分辨率。",
                "mediumThumbnailRes": "编辑器缩略图分辨率",
                "mediumThumbnailResDesc": "在编辑器中加载完整图像时显示的预览分辨率。"
            }
        }
    },
    "zh-TW": {
        "settings": {
            "processing": {
                "smallThumbnailRes": "網格縮圖解析度",
                "smallThumbnailResDesc": "圖庫網格中顯示的縮圖解析度。",
                "mediumThumbnailRes": "編輯器縮圖解析度",
                "mediumThumbnailResDesc": "在編輯器中載入完整影像時顯示的預覽解析度。"
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

    print("Starting translation updates for Thumbnail Resolution settings...")
    for lang, trans in TRANSLATIONS.items():
        file_path = LOCALES_DIR / f"{lang}.json"
        update_json_file(file_path, trans)
    print("Done!")

if __name__ == "__main__":
    main()
