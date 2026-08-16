import json
from pathlib import Path

LOCALES_DIR = Path("./locales")

TRANSLATIONS = {
    "ca": {
        "contextMenus": {
            "merge": {
                "title": "Fusionar",
                "focusStack": "Apilament d'enfocament"
            }
        },
        "modals": {
            "focusStack": {
                "title": "Apilament d'enfocament",
                "description": "Combina diverses imatges amb diferents distàncies d'enfocament en una sola imatge perfectament nítida.",
                "descriptionWithCount_one": "Combina {{count}} imatge amb diferents distàncies d'enfocament en una sola imatge perfectament nítida.",
                "descriptionWithCount_other": "Combina {{count}} imatges amb diferents distàncies d'enfocament en una sola imatge perfectament nítida.",
                "failed": "S'ha produït un error en l'apilament d'enfocament",
                "result": "Resultat",
                "depthMap": "Mapa de profunditat",
                "savedSuccess": "L'apilament d'enfocament s'ha desat correctament!",
                "stacking": "Apilant enfocament",
                "initializing": "Inicialitzant...",
                "close": "Tanca",
                "openInEditor": "Obre a l'editor",
                "cancel": "Cancel·la",
                "start": "Inicia",
                "save": "Desa"
            }
        }
    },
    "de": {
        "contextMenus": {
            "merge": {
                "title": "Zusammenfügen",
                "focusStack": "Fokus-Stacking"
            }
        },
        "modals": {
            "focusStack": {
                "title": "Fokus-Stacking",
                "description": "Kombinieren Sie mehrere Bilder mit unterschiedlichen Fokusdistanzen zu einem einzigen, perfekt scharfen Bild.",
                "descriptionWithCount_one": "Kombinieren Sie {{count}} Bild mit unterschiedlichen Fokusdistanzen zu einem einzigen, perfekt scharfen Bild.",
                "descriptionWithCount_other": "Kombinieren Sie {{count}} Bilder mit unterschiedlichen Fokusdistanzen zu einem einzigen, perfekt scharfen Bild.",
                "failed": "Fokus-Stacking fehlgeschlagen",
                "result": "Ergebnis",
                "depthMap": "Tiefenkarte",
                "savedSuccess": "Fokus-Stack erfolgreich gespeichert!",
                "stacking": "Fokus wird gestapelt",
                "initializing": "Wird initialisiert...",
                "close": "Schließen",
                "openInEditor": "Im Editor öffnen",
                "cancel": "Abbrechen",
                "start": "Start",
                "save": "Speichern"
            }
        }
    },
    "en": {
        "contextMenus": {
            "merge": {
                "title": "Merge",
                "focusStack": "Focus Stacking"
            }
        },
        "modals": {
            "focusStack": {
                "title": "Focus Stacking",
                "description": "Combine multiple images with varying focus distances into a single perfectly sharp image.",
                "descriptionWithCount_one": "Combine {{count}} image with varying focus distances into a single perfectly sharp image.",
                "descriptionWithCount_other": "Combine {{count}} images with varying focus distances into a single perfectly sharp image.",
                "failed": "Focus Stack Failed",
                "result": "Result",
                "depthMap": "Depth Map",
                "savedSuccess": "Focus Stack Saved Successfully!",
                "stacking": "Stacking Focus",
                "initializing": "Initializing...",
                "close": "Close",
                "openInEditor": "Open in Editor",
                "cancel": "Cancel",
                "start": "Start",
                "save": "Save"
            }
        }
    },
    "es": {
        "contextMenus": {
            "merge": {
                "title": "Combinar",
                "focusStack": "Apilamiento de enfoque"
            }
        },
        "modals": {
            "focusStack": {
                "title": "Apilamiento de enfoque",
                "description": "Combina varias imágenes con diferentes distancias de enfoque en una sola imagen perfectamente nítida.",
                "descriptionWithCount_one": "Combina {{count}} imagen con diferentes distancias de enfoque en una sola imagen perfectamente nítida.",
                "descriptionWithCount_other": "Combina {{count}} imágenes con diferentes distancias de enfoque en una sola imagen perfectamente nítida.",
                "failed": "Error en el apilamiento de enfoque",
                "result": "Resultado",
                "depthMap": "Mapa de profundidad",
                "savedSuccess": "¡Apilamiento de enfoque guardado con éxito!",
                "stacking": "Apilando enfoque",
                "initializing": "Inicializando...",
                "close": "Cerrar",
                "openInEditor": "Abrir en el editor",
                "cancel": "Cancelar",
                "start": "Iniciar",
                "save": "Guardar"
            }
        }
    },
    "fr": {
        "contextMenus": {
            "merge": {
                "title": "Fusionner",
                "focusStack": "Empilement de mise au point"
            }
        },
        "modals": {
            "focusStack": {
                "title": "Empilement de mise au point",
                "description": "Combinez plusieurs images avec des distances de mise au point variables en une seule image parfaitement nette.",
                "descriptionWithCount_one": "Combinez {{count}} image avec des distances de mise au point variables en une seule image parfaitement nette.",
                "descriptionWithCount_other": "Combinez {{count}} images avec des distances de mise au point variables en une seule image parfaitement nette.",
                "failed": "L'empilement de mise au point a échoué",
                "result": "Résultat",
                "depthMap": "Carte de profondeur",
                "savedSuccess": "Empilement de mise au point enregistré avec succès !",
                "stacking": "Empilement de la mise au point",
                "initializing": "Initialisation...",
                "close": "Fermer",
                "openInEditor": "Ouvrir dans l'éditeur",
                "cancel": "Annuler",
                "start": "Démarrer",
                "save": "Enregistrer"
            }
        }
    },
    "it": {
        "contextMenus": {
            "merge": {
                "title": "Unisci",
                "focusStack": "Focus Stacking"
            }
        },
        "modals": {
            "focusStack": {
                "title": "Focus Stacking",
                "description": "Combina più immagini con diverse distanze di messa a fuoco in un'unica immagine perfettamente nitida.",
                "descriptionWithCount_one": "Combina {{count}} immagine con diverse distanze di messa a fuoco in un'unica immagine perfettamente nitida.",
                "descriptionWithCount_other": "Combina {{count}} immagini con diverse distanze di messa a fuoco in un'unica immagine perfettamente nitida.",
                "failed": "Focus Stacking non riuscito",
                "result": "Risultato",
                "depthMap": "Mappa di profondità",
                "savedSuccess": "Focus Stack salvato con successo!",
                "stacking": "Unione messa a fuoco in corso",
                "initializing": "Inizializzazione...",
                "close": "Chiudi",
                "openInEditor": "Apri nell'editor",
                "cancel": "Annulla",
                "start": "Avvia",
                "save": "Salva"
            }
        }
    },
    "ja": {
        "contextMenus": {
            "merge": {
                "title": "結合",
                "focusStack": "フォーカススタッキング"
            }
        },
        "modals": {
            "focusStack": {
                "title": "フォーカススタッキング",
                "description": "ピント位置の異なる複数の画像を結合し、全体にピントが合った1枚の画像を作成します。",
                "descriptionWithCount_one": "ピント位置の異なる {{count}} 枚の画像を結合し、全体にピントが合った1枚の画像を作成します。",
                "descriptionWithCount_other": "ピント位置の異なる {{count}} 枚の画像を結合し、全体にピントが合った1枚の画像を作成します。",
                "failed": "フォーカススタッキングに失敗しました",
                "result": "結果",
                "depthMap": "深度マップ",
                "savedSuccess": "フォーカススタックを正常に保存しました！",
                "stacking": "フォーカスをスタック中",
                "initializing": "初期化中...",
                "close": "閉じる",
                "openInEditor": "エディターで開く",
                "cancel": "キャンセル",
                "start": "開始",
                "save": "保存"
            }
        }
    },
    "ko": {
        "contextMenus": {
            "merge": {
                "title": "병합",
                "focusStack": "포커스 스태킹"
            }
        },
        "modals": {
            "focusStack": {
                "title": "포커스 스태킹",
                "description": "초점 거리가 다른 여러 이미지를 결합하여 완벽하게 선명한 단일 이미지를 만듭니다.",
                "descriptionWithCount_one": "초점 거리가 다른 {{count}}개의 이미지를 결합하여 완벽하게 선명한 단일 이미지를 만듭니다.",
                "descriptionWithCount_other": "초점 거리가 다른 {{count}}개의 이미지를 결합하여 완벽하게 선명한 단일 이미지를 만듭니다.",
                "failed": "포커스 스태킹 실패",
                "result": "결과",
                "depthMap": "심도 맵",
                "savedSuccess": "포커스 스택이 성공적으로 저장되었습니다!",
                "stacking": "포커스 스태킹 중",
                "initializing": "초기화 중...",
                "close": "닫기",
                "openInEditor": "편집기에서 열기",
                "cancel": "취소",
                "start": "시작",
                "save": "저장"
            }
        }
    },
    "pl": {
        "contextMenus": {
            "merge": {
                "title": "Połącz",
                "focusStack": "Stosowanie ostrości (Focus Stacking)"
            }
        },
        "modals": {
            "focusStack": {
                "title": "Stosowanie ostrości",
                "description": "Połącz wiele obrazów z różnymi odległościami ostrości w jeden idealnie ostry obraz.",
                "descriptionWithCount_one": "Połącz {{count}} obraz z różnymi odległościami ostrości w jeden idealnie ostry obraz.",
                "descriptionWithCount_few": "Połącz {{count}} obrazy z różnymi odległościami ostrości w jeden idealnie ostry obraz.",
                "descriptionWithCount_many": "Połącz {{count}} obrazów z różnymi odległościami ostrości w jeden idealnie ostry obraz.",
                "descriptionWithCount_other": "Połącz {{count}} obrazów z różnymi odległościami ostrości w jeden idealnie ostry obraz.",
                "failed": "Złożenie ostrości nie powiodło się",
                "result": "Wynik",
                "depthMap": "Mapa głębi",
                "savedSuccess": "Stos ostrości zapisany pomyślnie!",
                "stacking": "Składanie ostrości",
                "initializing": "Inicjowanie...",
                "close": "Zamknij",
                "openInEditor": "Otwórz w edytorze",
                "cancel": "Anuluj",
                "start": "Rozpocznij",
                "save": "Zapisz"
            }
        }
    },
    "pt": {
        "contextMenus": {
            "merge": {
                "title": "Mesclar",
                "focusStack": "Empilhamento de Foco"
            }
        },
        "modals": {
            "focusStack": {
                "title": "Empilhamento de Foco",
                "description": "Combine várias imagens com diferentes distâncias de foco em uma única imagem perfeitamente nítida.",
                "descriptionWithCount_one": "Combine {{count}} imagem com diferentes distâncias de foco em uma única imagem perfeitamente nítida.",
                "descriptionWithCount_many": "Combine {{count}} imagens com diferentes distâncias de foco em uma única imagem perfeitamente nítida.",
                "descriptionWithCount_other": "Combine {{count}} imagens com diferentes distâncias de foco em uma única imagem perfeitamente nítida.",
                "failed": "Falha no Empilhamento de Foco",
                "result": "Resultado",
                "depthMap": "Mapa de Profundidade",
                "savedSuccess": "Empilhamento de foco salvo com sucesso!",
                "stacking": "Empilhando Foco",
                "initializing": "Inicializando...",
                "close": "Fechar",
                "openInEditor": "Abrir no Editor",
                "cancel": "Cancelar",
                "start": "Iniciar",
                "save": "Salvar"
            }
        }
    },
    "ru": {
        "contextMenus": {
            "merge": {
                "title": "Объединить",
                "focusStack": "Стекинг по фокусу"
            }
        },
        "modals": {
            "focusStack": {
                "title": "Стекинг по фокусу",
                "description": "Объедините несколько изображений с разным фокусным расстоянием в одно идеально резкое изображение.",
                "descriptionWithCount_one": "Объедините {{count}} изображение с разным фокусным расстоянием в одно идеально резкое изображение.",
                "descriptionWithCount_few": "Объедините {{count}} изображения с разным фокусным расстоянием в одно идеально резкое изображение.",
                "descriptionWithCount_many": "Объедините {{count}} изображений с разным фокусным расстоянием в одно идеально резкое изображение.",
                "descriptionWithCount_other": "Объедините {{count}} изображений с разным фокусным расстоянием в одно идеально резкое изображение.",
                "failed": "Стекинг по фокусу не удался",
                "result": "Результат",
                "depthMap": "Карта глубины",
                "savedSuccess": "Стек фокуса успешно сохранен!",
                "stacking": "Выполнение стекинга",
                "initializing": "Инициализация...",
                "close": "Закрыть",
                "openInEditor": "Открыть в редакторе",
                "cancel": "Отмена",
                "start": "Начать",
                "save": "Сохранить"
            }
        }
    },
    "zh-CN": {
        "contextMenus": {
            "merge": {
                "title": "合并",
                "focusStack": "焦距合成"
            }
        },
        "modals": {
            "focusStack": {
                "title": "焦距合成",
                "description": "将多张不同对焦距离的图像合并为一张完美清晰的图像。",
                "descriptionWithCount_one": "将 {{count}} 张不同对焦距离的图像合并为一张完美清晰的图像。",
                "descriptionWithCount_other": "将 {{count}} 张不同对焦距离的图像合并为一张完美清晰的图像。",
                "failed": "焦距合成失败",
                "result": "结果",
                "depthMap": "深度图",
                "savedSuccess": "焦距合成已成功保存！",
                "stacking": "正在合成焦距",
                "initializing": "正在初始化...",
                "close": "关闭",
                "openInEditor": "在编辑器中打开",
                "cancel": "取消",
                "start": "开始",
                "save": "保存"
            }
        }
    },
    "zh-TW": {
        "contextMenus": {
            "merge": {
                "title": "合併",
                "focusStack": "焦距合成"
            }
        },
        "modals": {
            "focusStack": {
                "title": "焦距合成",
                "description": "將多張不同對焦距離的影像合併為一張完美清晰的影像。",
                "descriptionWithCount_one": "將 {{count}} 張不同對焦距離的影像合併為一張完美清晰的影像。",
                "descriptionWithCount_other": "將 {{count}} 張不同對焦距離的影像合併為一張完美清晰的影像。",
                "failed": "焦距合成失敗",
                "result": "結果",
                "depthMap": "深度圖",
                "savedSuccess": "焦距合成已成功儲存！",
                "stacking": "正在合成焦距",
                "initializing": "正在初始化...",
                "close": "關閉",
                "openInEditor": "在編輯器中打開",
                "cancel": "取消",
                "start": "開始",
                "save": "儲存"
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

    print("Starting translation updates...")
    for lang, trans in TRANSLATIONS.items():
        file_path = LOCALES_DIR / f"{lang}.json"
        update_json_file(file_path, trans)
    print("Done!")

if __name__ == "__main__":
    main()
