import json
from pathlib import Path

LOCALES_DIR = Path("./locales")

TRANSLATIONS = {
    "ca": {
        "settings": {
            "data": {
                "resetLayoutButton": "Restablir disseny",
                "resetLayoutDesc": "Restaura els acoblaments de panells, els separadors laterals, les alçades i els commutadors de panells a la seva disposició predeterminada.",
                "resetLayoutTitle": "Restablir el disseny de l'espai de treball",
                "modals": {
                    "confirmResetLayout": "Restablir disseny",
                    "resetLayoutMessage": "Esteu segur que voleu restablir el disseny de l'espai de treball? Tots els panells acoblats, les amplades i les posicions dels commutadors es restauraran als seus valors predeterminats.",
                    "confirmResetLayoutTitle": "Restablir el disseny de l'espai de treball"
                },
                "statuses": {
                    "resettingLayout": "Restablint l'espai de treball...",
                    "layoutResetSuccess": "El disseny de l'espai de treball s'ha restablert."
                }
            }
        }
    },
    "de": {
        "settings": {
            "data": {
                "resetLayoutButton": "Layout zurücksetzen",
                "resetLayoutDesc": "Setzt Panel-Docks, seitliche Teiler, Höhen und Panel-Umschalter auf das Standard-Layout zurück.",
                "resetLayoutTitle": "Arbeitsbereich-Layout zurücksetzen",
                "modals": {
                    "confirmResetLayout": "Layout zurücksetzen",
                    "resetLayoutMessage": "Möchten Sie das Layout des Arbeitsbereichs wirklich zurücksetzen? Alle angedockten Panels, Breiten und Umschalter-Positionen werden auf ihre Standardwerte zurückgesetzt.",
                    "confirmResetLayoutTitle": "Arbeitsbereich-Layout zurücksetzen"
                },
                "statuses": {
                    "resettingLayout": "Arbeitsbereich wird zurückgesetzt...",
                    "layoutResetSuccess": "Layout des Arbeitsbereichs auf Standard zurückgesetzt."
                }
            }
        }
    },
    "en": {
        "settings": {
            "data": {
                "resetLayoutButton": "Reset Layout",
                "resetLayoutDesc": "Restore panel docks, side splitters, heights, and panel switchers to the default layout.",
                "resetLayoutTitle": "Reset Workspace Layout",
                "modals": {
                    "confirmResetLayout": "Reset Layout",
                    "resetLayoutMessage": "Are you sure you want to reset the workspace layout? All docked panels, widths, and switcher positions will be restored to their defaults.",
                    "confirmResetLayoutTitle": "Reset Workspace Layout"
                },
                "statuses": {
                    "resettingLayout": "Resetting workspace...",
                    "layoutResetSuccess": "Workspace layout reset to default."
                }
            }
        }
    },
    "es": {
        "settings": {
            "data": {
                "resetLayoutButton": "Restablecer diseño",
                "resetLayoutDesc": "Restaura los paneles acoplados, los divisores laterales, las alturas y los selectores de paneles a su disposición predeterminada.",
                "resetLayoutTitle": "Restablecer el diseño del espacio de trabajo",
                "modals": {
                    "confirmResetLayout": "Restablecer diseño",
                    "resetLayoutMessage": "¿Estás seguro de que deseas restablecer el diseño del espacio de trabajo? Todos los paneles acoplados, anchuras y posiciones de los selectores se restaurarán a sus valores predeterminados.",
                    "confirmResetLayoutTitle": "Restablecer el diseño del espacio de trabajo"
                },
                "statuses": {
                    "resettingLayout": "Restableciendo el espacio de trabajo...",
                    "layoutResetSuccess": "El diseño del espacio de trabajo se ha restablecido."
                }
            }
        }
    },
    "fr": {
        "settings": {
            "data": {
                "resetLayoutButton": "Réinitialiser la disposition",
                "resetLayoutDesc": "Restaure les panneaux ancrés, les séparateurs latéraux, les hauteurs et les sélecteurs de panneaux à leur disposition par défaut.",
                "resetLayoutTitle": "Réinitialiser la disposition de l'espace de travail",
                "modals": {
                    "confirmResetLayout": "Réinitialiser la disposition",
                    "resetLayoutMessage": "Êtes-vous sûr de vouloir réinitialiser la disposition de l'espace de travail ? Tous les panneaux ancrés, les largeurs et les positions des sélecteurs seront restaurés à leurs valeurs par défaut.",
                    "confirmResetLayoutTitle": "Réinitialiser la disposition de l'espace de travail"
                },
                "statuses": {
                    "resettingLayout": "Réinitialisation de l'espace de travail...",
                    "layoutResetSuccess": "La disposition de l'espace de travail a été réinitialisée."
                }
            }
        }
    },
    "it": {
        "settings": {
            "data": {
                "resetLayoutButton": "Ripristina layout",
                "resetLayoutDesc": "Ripristina i pannelli ancorati, i divisori laterali, le altezze e i selettori dei pannelli al layout predefinito.",
                "resetLayoutTitle": "Ripristina layout spazio di lavoro",
                "modals": {
                    "confirmResetLayout": "Ripristina layout",
                    "resetLayoutMessage": "Sei sicuro di voler ripristinare il layout dello spazio di lavoro? Tutti i pannelli ancorati, le larghezze e le posizioni dei selettori verranno ripristinati ai valori predefiniti.",
                    "confirmResetLayoutTitle": "Ripristina layout spazio di lavoro"
                },
                "statuses": {
                    "resettingLayout": "Ripristino dello spazio di lavoro...",
                    "layoutResetSuccess": "Layout dello spazio di lavoro ripristinato."
                }
            }
        }
    },
    "ja": {
        "settings": {
            "data": {
                "resetLayoutButton": "レイアウトをリセット",
                "resetLayoutDesc": "パネルのドック、サイドスプリッター、高さ、パネル切り替えボタンをデフォルトの配置に復元します。",
                "resetLayoutTitle": "ワークスペースレイアウトのリセット",
                "modals": {
                    "confirmResetLayout": "レイアウトをリセット",
                    "resetLayoutMessage": "ワークスペースのレイアウトをリセットしてもよろしいですか？ドッキングされたすべてのパネル、幅、および切り替えボタンの位置がデフォルトに復元されます。",
                    "confirmResetLayoutTitle": "ワークスペースレイアウトのリセット"
                },
                "statuses": {
                    "resettingLayout": "ワークスペースをリセット中...",
                    "layoutResetSuccess": "ワークスペースレイアウトがデフォルトにリセットされました。"
                }
            }
        }
    },
    "ko": {
        "settings": {
            "data": {
                "resetLayoutButton": "레이아웃 초기화",
                "resetLayoutDesc": "패널 도크, 측면 분할기, 높이 및 패널 전환기를 기본 레이아웃으로 복원합니다.",
                "resetLayoutTitle": "작업 공간 레이아웃 초기화",
                "modals": {
                    "confirmResetLayout": "레이아웃 초기화",
                    "resetLayoutMessage": "작업 공간 레이아웃을 초기화하시겠습니까? 도킹된 모든 패널, 너비 및 전환기 위치가 기본값으로 복원됩니다.",
                    "confirmResetLayoutTitle": "작업 공간 레이아웃 초기화"
                },
                "statuses": {
                    "resettingLayout": "작업 공간 초기화 중...",
                    "layoutResetSuccess": "작업 공간 레이아웃이 기본값으로 초기화되었습니다."
                }
            }
        }
    },
    "pl": {
        "settings": {
            "data": {
                "resetLayoutButton": "Zresetuj układ",
                "resetLayoutDesc": "Przywraca domyślny układ paneli, podziałów bocznych, wysokości oraz przełączników paneli.",
                "resetLayoutTitle": "Zresetuj układ obszaru roboczego",
                "modals": {
                    "confirmResetLayout": "Zresetuj układ",
                    "resetLayoutMessage": "Czy na pewno chcesz zresetować układ obszaru roboczego? Wszystkie przypięte panele, szerokości i pozycje przełączników zostaną przywrócone do wartości domyślnych.",
                    "confirmResetLayoutTitle": "Zresetuj układ obszaru roboczego"
                },
                "statuses": {
                    "resettingLayout": "Resetowanie obszaru roboczego...",
                    "layoutResetSuccess": "Układ obszaru roboczego został zresetowany do ustawień domyślnych."
                }
            }
        }
    },
    "pt": {
        "settings": {
            "data": {
                "resetLayoutButton": "Redefinir layout",
                "resetLayoutDesc": "Restaura os painéis acoplados, divisores laterais, alturas e seletores de painel para o layout padrão.",
                "resetLayoutTitle": "Redefinir layout do espaço de trabalho",
                "modals": {
                    "confirmResetLayout": "Redefinir layout",
                    "resetLayoutMessage": "Tem certeza de que deseja redefinir o layout do espaço de trabalho? Todos os painéis acoplados, larguras e posições dos seletores serão restaurados para os padrões originais.",
                    "confirmResetLayoutTitle": "Redefinir layout do espaço de trabalho"
                },
                "statuses": {
                    "resettingLayout": "Redefinando espaço de trabalho...",
                    "layoutResetSuccess": "O layout do espaço de trabalho foi redefinido para o padrão."
                }
            }
        }
    },
    "ru": {
        "settings": {
            "data": {
                "resetLayoutButton": "Сбросить макет",
                "resetLayoutDesc": "Восстанавливает стандартное расположение панелей, боковых разделителей, высоты и переключателей панелей.",
                "resetLayoutTitle": "Сбросить макет рабочей области",
                "modals": {
                    "confirmResetLayout": "Сбросить макет",
                    "resetLayoutMessage": "Вы уверены, что хотите сбросить макет рабочей области? Все закрепленные панели, ширина и позиции переключателей будут восстановлены по умолчанию.",
                    "confirmResetLayoutTitle": "Сбросить макет рабочей области"
                },
                "statuses": {
                    "resettingLayout": "Сброс рабочей области...",
                    "layoutResetSuccess": "Макет рабочей области сброшен по умолчанию."
                }
            }
        }
    },
    "zh-CN": {
        "settings": {
            "data": {
                "resetLayoutButton": "重置布局",
                "resetLayoutDesc": "将面板停靠区、侧边分割条、高度和面板切换器恢复为默认布局。",
                "resetLayoutTitle": "重置工作区布局",
                "modals": {
                    "confirmResetLayout": "重置布局",
                    "resetLayoutMessage": "是否确定要重置工作区布局？所有停靠的面板、宽度和切换器位置都将恢复为默认值。",
                    "confirmResetLayoutTitle": "重置工作区布局"
                },
                "statuses": {
                    "resettingLayout": "正在重置工作区...",
                    "layoutResetSuccess": "工作区布局已重置为默认值。"
                }
            }
        }
    },
    "zh-TW": {
        "settings": {
            "data": {
                "resetLayoutButton": "重設版面配置",
                "resetLayoutDesc": "將面板停靠區、側邊分割條、高度和面板切換器還原為預設的版面配置。",
                "resetLayoutTitle": "重設工作區版面配置",
                "modals": {
                    "confirmResetLayout": "重設版面配置",
                    "resetLayoutMessage": "確定要重設工作區版面配置嗎？所有停靠的面板、寬度和切換器位置都將還原為預設值。",
                    "confirmResetLayoutTitle": "重設工作區版面配置"
                },
                "statuses": {
                    "resettingLayout": "正在重設工作區...",
                    "layoutResetSuccess": "工作區版面配置已重設為預設值。"
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

    print("Starting translation updates for workspace layout reset...")
    for lang, trans in TRANSLATIONS.items():
        file_path = LOCALES_DIR / f"{lang}.json"
        update_json_file(file_path, trans)
    print("Done!")

if __name__ == "__main__":
    main()
