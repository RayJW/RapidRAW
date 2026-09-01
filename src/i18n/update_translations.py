import json
from pathlib import Path

LOCALES_DIR = Path("./locales")

TRANSLATIONS = {
    "ca": {
        "editor": {
            "guided": {
                "hint": "Dibuixa al llarg de les vores de la foto que haurien de ser verticals o horitzontals.",
                "linesStatus": "Línies guia actives",
                "toast": {
                    "angleRejected": "L'angle de la línia està massa lluny de l'horitzontal o vertical",
                    "maxLines": "Es permeten com a màxim 2 línies verticals i 2 horitzontals"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "Perspectiva guiada"
                }
            },
            "transform": {
                "guided": "Perspectiva guiada",
                "manual": "Transformació manual"
            }
        }
    },
    "de": {
        "editor": {
            "guided": {
                "hint": "Zeichnen Sie entlang der Kanten in Ihrem Foto, die vertikal oder horizontal sein sollten.",
                "linesStatus": "Aktive Hilfslinien",
                "toast": {
                    "angleRejected": "Linienwinkel ist zu weit von horizontal oder vertikal entfernt",
                    "maxLines": "Maximal 2 vertikale und 2 horizontale Linien erlaubt"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "Geführte Perspektive"
                }
            },
            "transform": {
                "guided": "Geführte Perspektive",
                "manual": "Manuelle Transformation"
            }
        }
    },
    "en": {
        "editor": {
            "guided": {
                "hint": "Draw along edges in your photo that should be vertical or horizontal.",
                "linesStatus": "Active Guide Lines",
                "toast": {
                    "angleRejected": "Line angle is too far from horizontal or vertical",
                    "maxLines": "Maximum 2 vertical and 2 horizontal lines allowed"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "Guided Perspective"
                }
            },
            "transform": {
                "guided": "Guided Perspective",
                "manual": "Manual Transform"
            }
        }
    },
    "es": {
        "editor": {
            "guided": {
                "hint": "Dibuja a lo largo de los bordes de tu foto que deberían ser verticales u horizontales.",
                "linesStatus": "Líneas guía activas",
                "toast": {
                    "angleRejected": "El ángulo de la línea está demasiado lejos de la horizontal o vertical",
                    "maxLines": "Se permiten un máximo de 2 líneas verticales y 2 horizontales"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "Perspectiva guiada"
                }
            },
            "transform": {
                "guided": "Perspectiva guiada",
                "manual": "Transformación manual"
            }
        }
    },
    "fr": {
        "editor": {
            "guided": {
                "hint": "Tracez le long des bords de votre photo qui devraient être verticaux ou horizontaux.",
                "linesStatus": "Lignes de guidage actives",
                "toast": {
                    "angleRejected": "L'angle de la ligne est trop éloigné de l'horizontale ou de la verticale",
                    "maxLines": "Maximum de 2 lignes verticales et 2 lignes horizontales autorisées"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "Perspective guidée"
                }
            },
            "transform": {
                "guided": "Perspective guidée",
                "manual": "Transformation manuelle"
            }
        }
    },
    "it": {
        "editor": {
            "guided": {
                "hint": "Disegna lungo i bordi della tua foto che dovrebbero essere verticali o orizzontali.",
                "linesStatus": "Linee guida attive",
                "toast": {
                    "angleRejected": "L'angolo della linea è troppo lontano dall'orizzontale o verticale",
                    "maxLines": "Sono consentite massimo 2 linee verticali e 2 orizzontali"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "Prospettiva guidata"
                }
            },
            "transform": {
                "guided": "Prospettiva guidata",
                "manual": "Trasformazione manuale"
            }
        }
    },
    "ja": {
        "editor": {
            "guided": {
                "hint": "垂直または水平であるべき写真の縁に沿って描画します。",
                "linesStatus": "アクティブなガイドライン",
                "toast": {
                    "angleRejected": "線の角度が水平または垂直から離れすぎています",
                    "maxLines": "垂直線と水平線はそれぞれ最大2本まで許可されています"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "ガイド付きパースペクティブ"
                }
            },
            "transform": {
                "guided": "ガイド付きパースペクティブ",
                "manual": "手動変形"
            }
        }
    },
    "ko": {
        "editor": {
            "guided": {
                "hint": "사진에서 수직이나 수평이 되어야 하는 가장자리를 따라 그리세요.",
                "linesStatus": "활성 안내선",
                "toast": {
                    "angleRejected": "선의 각도가 수평이나 수직에서 너무 벗어났습니다",
                    "maxLines": "수직선 2개, 수평선 2개까지만 허용됩니다"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "유도된 원근 보정"
                }
            },
            "transform": {
                "guided": "유도된 원근 보정",
                "manual": "수동 변형"
            }
        }
    },
    "pl": {
        "editor": {
            "guided": {
                "hint": "Rysuj wzdłuż krawędzi na zdjęciu, które powinny być pionowe lub poziome.",
                "linesStatus": "Aktywne linie pomocnicze",
                "toast": {
                    "angleRejected": "Kąt linii jest zbyt odległy od poziomu lub pionu",
                    "maxLines": "Dozwolone są maksymalnie 2 linie pionowe i 2 poziome"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "Perspektywa z przewodnikiem"
                }
            },
            "transform": {
                "guided": "Perspektywa z przewodnikiem",
                "manual": "Ręczne przekształcenie"
            }
        }
    },
    "pt": {
        "editor": {
            "guided": {
                "hint": "Desenhe ao longo das bordas da sua foto que devem ser verticais ou horizontais.",
                "linesStatus": "Linhas guias ativas",
                "toast": {
                    "angleRejected": "O ângulo da linha está muito longe da horizontal ou vertical",
                    "maxLines": "São permitidas no máximo 2 linhas verticais e 2 horizontais"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "Perspectiva guiada"
                }
            },
            "transform": {
                "guided": "Perspectiva guiada",
                "manual": "Transformação manual"
            }
        }
    },
    "ru": {
        "editor": {
            "guided": {
                "hint": "Нарисуйте вдоль краев на фото, которые должны быть вертикальными или горизонтальными.",
                "linesStatus": "Активные направляющие",
                "toast": {
                    "angleRejected": "Угол линии слишком далек от горизонтали или вертикали",
                    "maxLines": "Допускается максимум 2 вертикальные и 2 горизонтальные линии"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "Направляемая перспектива"
                }
            },
            "transform": {
                "guided": "Направляемая перспектива",
                "manual": "Ручная трансформация"
            }
        }
    },
    "zh-CN": {
        "editor": {
            "guided": {
                "hint": "沿着照片中应该是垂直或水平的边缘绘制。",
                "linesStatus": "活跃引导线",
                "toast": {
                    "angleRejected": "线条角度偏离水平或垂直太远",
                    "maxLines": "最多允许 2 条垂直线和 2 条水平线"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "引导透视"
                }
            },
            "transform": {
                "guided": "引导透视",
                "manual": "手动变换"
            }
        }
    },
    "zh-TW": {
        "editor": {
            "guided": {
                "hint": "沿著照片中應該是垂直或水平的邊緣繪製。",
                "linesStatus": "活躍引導線",
                "toast": {
                    "angleRejected": "線條角度偏離水平或垂直太遠",
                    "maxLines": "最多允許 2 條垂直線和 2 條水平線"
                }
            }
        },
        "modals": {
            "copyPaste": {
                "groups": {
                    "guidedPerspective": "引導透視"
                }
            },
            "transform": {
                "guided": "引導透視",
                "manual": "手動變換"
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

    print("Starting translation updates for Guided Perspective...")
    for lang, trans in TRANSLATIONS.items():
        file_path = LOCALES_DIR / f"{lang}.json"
        update_json_file(file_path, trans)
    print("Done!")

if __name__ == "__main__":
    main()
