import json
from pathlib import Path

LOCALES_DIR = Path("./locales")

TRANSLATIONS = {
    "ca": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "Captura connectada"
                }
            }
        },
        "tethering": {
            "title": "Captura connectada",
            "scanTooltip": "Cerca càmeres",
            "status": "Estat",
            "cameraConnected": "Càmera connectada",
            "selectCamera": "Selecciona càmera",
            "startLiveView": "Inicia vista en directe",
            "stopLiveView": "Atura vista en directe",
            "noCameraDetected": "Cap càmera detectada",
            "liveViewAlt": "Vista en directe",
            "ghostOverlayAlt": "Superposició fantasma",
            "overlayOff": "Desactivat",
            "rotate90": "Gira 90°",
            "flipHorizontal": "Inverteix horitzontalment",
            "overlayLastShot": "Superposa l'última captura",
            "selectCameraPlaceholder": "Selecciona una càmera",
            "noCamerasFound": "No s'han trobat càmeres. Assegura't que està connectada i en mode PC Remote.",
            "connectCamera": "Connecta la càmera",
            "exposureSettings": "Ajustaments d'exposició",
            "shutter": "Obturador",
            "aperture": "Obertura",
            "iso": "ISO",
            "whiteBalance": "Balanç de blancs",
            "shutterPlaceholder": "p. ex. 1/200",
            "aperturePlaceholder": "p. ex. 2.8",
            "isoPlaceholder": "p. ex. 400",
            "autoOpenCaptured": "Obre automàticament la imatge capturada",
            "capturing": "Capturant...",
            "triggerCapture": "Dispara captura",
            "toasts": {
                "noCamerasFound": "No s'han trobat càmeres. Assegura't que està en mode PC Remote.",
                "detectionFailed": "Error en la detecció: {{err}}",
                "communicationFailed": "Error en comunicar-se amb la càmera",
                "connectionFailed": "Connexió fallida: {{err}}",
                "setFailed": "Error en configurar {{key}}: {{err}}",
                "selectFolderFirst": "Selecciona primer una carpeta estàndard a la biblioteca.",
                "captureFailed": "Error en la captura: {{err}}",
                "cameraDisconnected": "Càmera desconnectada"
            }
        }
    },
    "de": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "Tethering"
                }
            }
        },
        "tethering": {
            "title": "Tethering",
            "scanTooltip": "Nach Kameras suchen",
            "status": "Status",
            "cameraConnected": "Kamera verbunden",
            "selectCamera": "Kamera auswählen",
            "startLiveView": "Live-View starten",
            "stopLiveView": "Live-View beenden",
            "noCameraDetected": "Keine Kamera erkannt",
            "liveViewAlt": "Live-View",
            "ghostOverlayAlt": "Geister-Überlagerung",
            "overlayOff": "Aus",
            "rotate90": "90° drehen",
            "flipHorizontal": "Horizontal spiegeln",
            "overlayLastShot": "Letzte Aufnahme überlagern",
            "selectCameraPlaceholder": "Eine Kamera auswählen",
            "noCamerasFound": "Keine Kameras gefunden. Stellen Sie sicher, dass sie angeschlossen und im PC-Fernsteuerungsmodus ist.",
            "connectCamera": "Kamera verbinden",
            "exposureSettings": "Belichtungseinstellungen",
            "shutter": "Verschluss",
            "aperture": "Blende",
            "iso": "ISO",
            "whiteBalance": "Weißabgleich",
            "shutterPlaceholder": "z. B. 1/200",
            "aperturePlaceholder": "z. B. 2.8",
            "isoPlaceholder": "z. B. 400",
            "autoOpenCaptured": "Aufgenommenes Bild autom. öffnen",
            "capturing": "Aufnahme läuft...",
            "triggerCapture": "Auslösen",
            "toasts": {
                "noCamerasFound": "Keine Kameras gefunden. Stellen Sie sicher, dass sie im PC-Fernsteuerungsmodus ist.",
                "detectionFailed": "Erkennung fehlgeschlagen: {{err}}",
                "communicationFailed": "Kommunikation mit der Kamera fehlgeschlagen",
                "connectionFailed": "Verbindung fehlgeschlagen: {{err}}",
                "setFailed": "Fehler beim Einstellen von {{key}}: {{err}}",
                "selectFolderFirst": "Bitte wählen Sie zuerst einen Standardordner in Ihrer Bibliothek aus.",
                "captureFailed": "Aufnahme fehlgeschlagen: {{err}}",
                "cameraDisconnected": "Kamera getrennt"
            }
        }
    },
    "en": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "Tethering"
                }
            }
        },
        "tethering": {
            "title": "Tethering",
            "scanTooltip": "Scan for Cameras",
            "status": "Status",
            "cameraConnected": "Camera Connected",
            "selectCamera": "Select Camera",
            "startLiveView": "Start Live View",
            "stopLiveView": "Stop Live View",
            "noCameraDetected": "No camera detected",
            "liveViewAlt": "Live View",
            "ghostOverlayAlt": "Ghost Overlay",
            "overlayOff": "Off",
            "rotate90": "Rotate 90°",
            "flipHorizontal": "Flip Horizontal",
            "overlayLastShot": "Overlay Last Shot",
            "selectCameraPlaceholder": "Select a camera",
            "noCamerasFound": "No cameras found. Ensure it is connected and in PC Remote mode.",
            "connectCamera": "Connect Camera",
            "exposureSettings": "Exposure Settings",
            "shutter": "Shutter",
            "aperture": "Aperture",
            "iso": "ISO",
            "whiteBalance": "White Balance",
            "shutterPlaceholder": "e.g. 1/200",
            "aperturePlaceholder": "e.g. 2.8",
            "isoPlaceholder": "e.g. 400",
            "autoOpenCaptured": "Auto-open captured image",
            "capturing": "Capturing...",
            "triggerCapture": "Trigger Capture",
            "toasts": {
                "noCamerasFound": "No cameras found. Ensure it is in PC Remote mode.",
                "detectionFailed": "Detection failed: {{err}}",
                "communicationFailed": "Failed to communicate with camera",
                "connectionFailed": "Connection failed: {{err}}",
                "setFailed": "Failed to set {{key}}: {{err}}",
                "selectFolderFirst": "Please select a standard folder in your Library first.",
                "captureFailed": "Capture failed: {{err}}",
                "cameraDisconnected": "Camera disconnected"
            }
        }
    },
    "es": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "Captura conectada"
                }
            }
        },
        "tethering": {
            "title": "Captura conectada",
            "scanTooltip": "Buscar cámaras",
            "status": "Estado",
            "cameraConnected": "Cámara conectada",
            "selectCamera": "Seleccionar cámara",
            "startLiveView": "Iniciar vista en vivo",
            "stopLiveView": "Detener vista en vivo",
            "noCameraDetected": "No se detectó ninguna cámara",
            "liveViewAlt": "Vista en vivo",
            "ghostOverlayAlt": "Superposición fantasma",
            "overlayOff": "Desactivado",
            "rotate90": "Girar 90°",
            "flipHorizontal": "Voltear horizontalmente",
            "overlayLastShot": "Superponer última captura",
            "selectCameraPlaceholder": "Seleccionar una cámara",
            "noCamerasFound": "No se encontraron cámaras. Asegúrate de que esté conectada y en modo PC Remote.",
            "connectCamera": "Conectar cámara",
            "exposureSettings": "Ajustes de exposición",
            "shutter": "Obturador",
            "aperture": "Apertura",
            "iso": "ISO",
            "whiteBalance": "Balance de blancos",
            "shutterPlaceholder": "ej. 1/200",
            "aperturePlaceholder": "ej. 2.8",
            "isoPlaceholder": "ej. 400",
            "autoOpenCaptured": "Abrir imagen capturada automáticamente",
            "capturing": "Capturando...",
            "triggerCapture": "Disparar captura",
            "toasts": {
                "noCamerasFound": "No se encontraron cámaras. Asegúrate de que esté en modo PC Remote.",
                "detectionFailed": "Error en la detección: {{err}}",
                "communicationFailed": "Error al comunicarse con la cámara",
                "connectionFailed": "Error de conexión: {{err}}",
                "setFailed": "Error al configurar {{key}}: {{err}}",
                "selectFolderFirst": "Por favor, selecciona primero una carpeta estándar en tu biblioteca.",
                "captureFailed": "Error en la captura: {{err}}",
                "cameraDisconnected": "Cámara desconectada"
            }
        }
    },
    "fr": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "Prise de vue connectée"
                }
            }
        },
        "tethering": {
            "title": "Prise de vue connectée",
            "scanTooltip": "Rechercher des appareils",
            "status": "État",
            "cameraConnected": "Appareil connecté",
            "selectCamera": "Sélectionner un appareil",
            "startLiveView": "Démarrer la visée directe",
            "stopLiveView": "Arrêter la visée directe",
            "noCameraDetected": "Aucun appareil détecté",
            "liveViewAlt": "Visée directe",
            "ghostOverlayAlt": "Incrustation fantôme",
            "overlayOff": "Désactivé",
            "rotate90": "Faire pivoter de 90°",
            "flipHorizontal": "Retourner horizontalement",
            "overlayLastShot": "Superposer la dernière photo",
            "selectCameraPlaceholder": "Sélectionner un appareil",
            "noCamerasFound": "Aucun appareil trouvé. Assurez-vous qu'il est connecté et en mode PC Remote.",
            "connectCamera": "Connecter l'appareil",
            "exposureSettings": "Paramètres d'exposition",
            "shutter": "Obturateur",
            "aperture": "Ouverture",
            "iso": "ISO",
            "whiteBalance": "Balance des blancs",
            "shutterPlaceholder": "ex. 1/200",
            "aperturePlaceholder": "ex. 2.8",
            "isoPlaceholder": "ex. 400",
            "autoOpenCaptured": "Ouvrir automatiquement l'image capturée",
            "capturing": "Capture en cours...",
            "triggerCapture": "Déclencher la capture",
            "toasts": {
                "noCamerasFound": "Aucun appareil trouvé. Assurez-vous qu'il est en mode PC Remote.",
                "detectionFailed": "Échec de la détection : {{err}}",
                "communicationFailed": "Échec de la communication avec l'appareil",
                "connectionFailed": "Échec de la connexion : {{err}}",
                "setFailed": "Échec de la définition de {{key}} : {{err}}",
                "selectFolderFirst": "Veuillez d'abord sélectionner un dossier standard dans votre bibliothèque.",
                "captureFailed": "Échec de la capture : {{err}}",
                "cameraDisconnected": "Appareil déconnecté"
            }
        }
    },
    "it": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "Acquisizione diretta"
                }
            }
        },
        "tethering": {
            "title": "Acquisizione diretta",
            "scanTooltip": "Cerca fotocamere",
            "status": "Stato",
            "cameraConnected": "Fotocamera connessa",
            "selectCamera": "Seleziona fotocamera",
            "startLiveView": "Avvia Live View",
            "stopLiveView": "Interrompi Live View",
            "noCameraDetected": "Nessuna fotocamera rilevata",
            "liveViewAlt": "Live View",
            "ghostOverlayAlt": "Sovrapposizione fantasma",
            "overlayOff": "Spento",
            "rotate90": "Ruota di 90°",
            "flipHorizontal": "Capovolgi orizzontalmente",
            "overlayLastShot": "Sovrapponi ultimo scatto",
            "selectCameraPlaceholder": "Seleziona una fotocamera",
            "noCamerasFound": "Nessuna fotocamera trovata. Assicurati che sia collegata e in modalità PC Remote.",
            "connectCamera": "Connetti fotocamera",
            "exposureSettings": "Impostazioni di esposizione",
            "shutter": "Otturatore",
            "aperture": "Apertura",
            "iso": "ISO",
            "whiteBalance": "Bilanciamento del bianco",
            "shutterPlaceholder": "es. 1/200",
            "aperturePlaceholder": "es. 2.8",
            "isoPlaceholder": "es. 400",
            "autoOpenCaptured": "Apri automaticamente l'immagine acquisita",
            "capturing": "Acquisizione in corso...",
            "triggerCapture": "Scatta foto",
            "toasts": {
                "noCamerasFound": "Nessuna fotocamera trovata. Assicurati che sia in modalità PC Remote.",
                "detectionFailed": "Rilevamento non riuscito: {{err}}",
                "communicationFailed": "Comunicazione con la fotocamera non riuscita",
                "connectionFailed": "Connessione non riuscita: {{err}}",
                "setFailed": "Impossibile impostare {{key}}: {{err}}",
                "selectFolderFirst": "Seleziona prima una cartella standard nella tua libreria.",
                "captureFailed": "Acquisizione non riuscita: {{err}}",
                "cameraDisconnected": "Fotocamera disconnessa"
            }
        }
    },
    "ja": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "テザー撮影"
                }
            }
        },
        "tethering": {
            "title": "テザー撮影",
            "scanTooltip": "カメラをスキャン",
            "status": "ステータス",
            "cameraConnected": "カメラ接続中",
            "selectCamera": "カメラを選択",
            "startLiveView": "ライブビュー開始",
            "stopLiveView": "ライブビュー停止",
            "noCameraDetected": "カメラが検出されません",
            "liveViewAlt": "ライブビュー",
            "ghostOverlayAlt": "ゴーストオーバーレイ",
            "overlayOff": "オフ",
            "rotate90": "90°回転",
            "flipHorizontal": "左右反転",
            "overlayLastShot": "直前のショットをオーバーレイ",
            "selectCameraPlaceholder": "カメラを選択してください",
            "noCamerasFound": "カメラが見つかりません。接続とPCリモートモードを確認してください。",
            "connectCamera": "カメラを接続",
            "exposureSettings": "露出設定",
            "shutter": "シャッター",
            "aperture": "絞り",
            "iso": "ISO",
            "whiteBalance": "ホワイトバランス",
            "shutterPlaceholder": "例: 1/200",
            "aperturePlaceholder": "例: 2.8",
            "isoPlaceholder": "例: 400",
            "autoOpenCaptured": "撮影した画像を自動で開く",
            "capturing": "撮影中...",
            "triggerCapture": "撮影を実行",
            "toasts": {
                "noCamerasFound": "カメラが見つかりません。PCリモートモードになっていることを確認してください。",
                "detectionFailed": "検出に失敗しました: {{err}}",
                "communicationFailed": "カメラとの通信に失敗しました",
                "connectionFailed": "接続に失敗しました: {{err}}",
                "setFailed": "{{key}} の設定に失敗しました: {{err}}",
                "selectFolderFirst": "最初にライブラリで通常のフォルダを選択してください。",
                "captureFailed": "撮影に失敗しました: {{err}}",
                "cameraDisconnected": "カメラが切断されました"
            }
        }
    },
    "ko": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "테더링"
                }
            }
        },
        "tethering": {
            "title": "테더링",
            "scanTooltip": "카메라 검색",
            "status": "상태",
            "cameraConnected": "카메라 연결됨",
            "selectCamera": "카메라 선택",
            "startLiveView": "라이브 뷰 시작",
            "stopLiveView": "라이브 뷰 중지",
            "noCameraDetected": "감지된 카메라 없음",
            "liveViewAlt": "라이브 뷰",
            "ghostOverlayAlt": "고스트 오버레이",
            "overlayOff": "끄기",
            "rotate90": "90° 회전",
            "flipHorizontal": "좌우 대칭",
            "overlayLastShot": "이전 촬영 오버레이",
            "selectCameraPlaceholder": "카메라를 선택하세요",
            "noCamerasFound": "카메라를 찾을 수 없습니다. 연결 상태와 PC 원격 모드를 확인하세요.",
            "connectCamera": "카메라 연결",
            "exposureSettings": "노출 설정",
            "shutter": "셔터",
            "aperture": "조리개",
            "iso": "ISO",
            "whiteBalance": "화이트 밸런스",
            "shutterPlaceholder": "예: 1/200",
            "aperturePlaceholder": "예: 2.8",
            "isoPlaceholder": "예: 400",
            "autoOpenCaptured": "촬영된 이미지 자동으로 열기",
            "capturing": "촬영 중...",
            "triggerCapture": "촬영 실행",
            "toasts": {
                "noCamerasFound": "카메라를 찾을 수 없습니다. PC 원격 모드인지 확인하세요.",
                "detectionFailed": "감지 실패: {{err}}",
                "communicationFailed": "카메라와 통신하지 못했습니다",
                "connectionFailed": "연결 실패: {{err}}",
                "setFailed": "{{key}} 설정 실패: {{err}}",
                "selectFolderFirst": "라이브러리에서 먼저 일반 폴더를 선택하세요.",
                "captureFailed": "촬영 실패: {{err}}",
                "cameraDisconnected": "카메라 연결이 끊어졌습니다"
            }
        }
    },
    "pl": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "Tethering (Połączenie przewodowe)"
                }
            }
        },
        "tethering": {
            "title": "Tethering",
            "scanTooltip": "Szukaj aparatów",
            "status": "Status",
            "cameraConnected": "Aparat połączony",
            "selectCamera": "Wybierz aparat",
            "startLiveView": "Uruchom Live View",
            "stopLiveView": "Zatrzymaj Live View",
            "noCameraDetected": "Nie wykryto aparatu",
            "liveViewAlt": "Live View",
            "ghostOverlayAlt": "Nakładka poprzedniego zdjęcia",
            "overlayOff": "Wył.",
            "rotate90": "Obróć o 90°",
            "flipHorizontal": "Obróć w poziomie",
            "overlayLastShot": "Nałóż ostatnie zdjęcie",
            "selectCameraPlaceholder": "Wybierz aparat",
            "noCamerasFound": "Nie znaleziono aparatów. Upewnij się, że aparat jest podłączony i działa w trybie PC Remote.",
            "connectCamera": "Połącz aparat",
            "exposureSettings": "Ustawienia ekspozycji",
            "shutter": "Migawka",
            "aperture": "Przysłona",
            "iso": "ISO",
            "whiteBalance": "Balans bieli",
            "shutterPlaceholder": "np. 1/200",
            "aperturePlaceholder": "np. 2.8",
            "isoPlaceholder": "np. 400",
            "autoOpenCaptured": "Automatycznie otwieraj zrobione zdjęcie",
            "capturing": "Robienie zdjęcia...",
            "triggerCapture": "Wyzwól migawkę",
            "toasts": {
                "noCamerasFound": "Nie znaleziono aparatów. Upewnij się, że włączono tryb PC Remote.",
                "detectionFailed": "Wykrywanie nie powiodło się: {{err}}",
                "communicationFailed": "Błąd komunikacji z aparatem",
                "connectionFailed": "Połączenie nie powiodło się: {{err}}",
                "setFailed": "Nie udało się ustawić {{key}}: {{err}}",
                "selectFolderFirst": "Najpierw wybierz standardowy folder w bibliotece.",
                "captureFailed": "Przechwytywanie nie powiodło się: {{err}}",
                "cameraDisconnected": "Aparat został odłączony"
            }
        }
    },
    "pt": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "Captura Conectada (Tethering)"
                }
            }
        },
        "tethering": {
            "title": "Tethering",
            "scanTooltip": "Buscar Câmeras",
            "status": "Status",
            "cameraConnected": "Câmera Conectada",
            "selectCamera": "Selecionar Câmera",
            "startLiveView": "Iniciar Live View",
            "stopLiveView": "Parar Live View",
            "noCameraDetected": "Nenhuma câmera detectada",
            "liveViewAlt": "Live View",
            "ghostOverlayAlt": "Sobreposição Fantasma",
            "overlayOff": "Desligado",
            "rotate90": "Girar 90°",
            "flipHorizontal": "Espelhar Horizontalmente",
            "overlayLastShot": "Sobrepor Última Foto",
            "selectCameraPlaceholder": "Selecione uma câmera",
            "noCamerasFound": "Nenhuma câmera encontrada. Certifique-se de que esteja conectada e no modo PC Remote.",
            "connectCamera": "Conectar Câmera",
            "exposureSettings": "Configurações de Exposição",
            "shutter": "Obturador",
            "aperture": "Abertura",
            "iso": "ISO",
            "whiteBalance": "Balanço de Branco",
            "shutterPlaceholder": "ex. 1/200",
            "aperturePlaceholder": "ex. 2.8",
            "isoPlaceholder": "ex. 400",
            "autoOpenCaptured": "Abrir automaticamente imagem capturada",
            "capturing": "Capturando...",
            "triggerCapture": "Disparar Captura",
            "toasts": {
                "noCamerasFound": "Nenhuma câmera encontrada. Verifique se está no modo PC Remote.",
                "detectionFailed": "Falha na detecção: {{err}}",
                "communicationFailed": "Falha na comunicação com a câmera",
                "connectionFailed": "Falha na conexão: {{err}}",
                "setFailed": "Falha ao definir {{key}}: {{err}}",
                "selectFolderFirst": "Selecione uma pasta padrão na sua Biblioteca primeiro.",
                "captureFailed": "Falha na captura: {{err}}",
                "cameraDisconnected": "Câmera desconectada"
            }
        }
    },
    "ru": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "Съемка на ПК (Тетеринг)"
                }
            }
        },
        "tethering": {
            "title": "Тетеринг",
            "scanTooltip": "Поиск камер",
            "status": "Статус",
            "cameraConnected": "Камера подключена",
            "selectCamera": "Выбрать камеру",
            "startLiveView": "Запустить Live View",
            "stopLiveView": "Остановить Live View",
            "noCameraDetected": "Камера не обнаружена",
            "liveViewAlt": "Live View",
            "ghostOverlayAlt": "Полупрозрачное наложение",
            "overlayOff": "Выкл.",
            "rotate90": "Повернуть на 90°",
            "flipHorizontal": "Отразить по горизонтали",
            "overlayLastShot": "Наложить прошлый снимок",
            "selectCameraPlaceholder": "Выберите камеру",
            "noCamerasFound": "Камеры не найдены. Убедитесь, что камера подключена и включен режим ПК.",
            "connectCamera": "Подключить камеру",
            "exposureSettings": "Настройки экспозиции",
            "shutter": "Выдержка",
            "aperture": "Диафрагма",
            "iso": "ISO",
            "whiteBalance": "Баланс белого",
            "shutterPlaceholder": "напр. 1/200",
            "aperturePlaceholder": "напр. 2.8",
            "isoPlaceholder": "напр. 400",
            "autoOpenCaptured": "Автоматически открывать снимок",
            "capturing": "Съемка...",
            "triggerCapture": "Сделать снимок",
            "toasts": {
                "noCamerasFound": "Камеры не найдены. Убедитесь, что включен режим дистанционного управления ПК.",
                "detectionFailed": "Ошибка обнаружения: {{err}}",
                "communicationFailed": "Не удалось связаться с камерой",
                "connectionFailed": "Ошибка подключения: {{err}}",
                "setFailed": "Не удалось установить {{key}}: {{err}}",
                "selectFolderFirst": "Сначала выберите стандартную папку в Библиотеке.",
                "captureFailed": "Ошибка съемки: {{err}}",
                "cameraDisconnected": "Камера отключена"
            }
        }
    },
    "zh-CN": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "联机拍摄"
                }
            }
        },
        "tethering": {
            "title": "联机拍摄",
            "scanTooltip": "扫描相机",
            "status": "状态",
            "cameraConnected": "相机已连接",
            "selectCamera": "选择相机",
            "startLiveView": "开启实时取景",
            "stopLiveView": "停止实时取景",
            "noCameraDetected": "未检测到相机",
            "liveViewAlt": "实时取景",
            "ghostOverlayAlt": "叠图预览",
            "overlayOff": "关闭",
            "rotate90": "旋转 90°",
            "flipHorizontal": "水平翻转",
            "overlayLastShot": "叠加上一张拍摄照片",
            "selectCameraPlaceholder": "选择一台相机",
            "noCamerasFound": "未找到相机。请确保已连接并处于 PC 遥控模式。",
            "connectCamera": "连接相机",
            "exposureSettings": "曝光设置",
            "shutter": "快门",
            "aperture": "光圈",
            "iso": "ISO",
            "whiteBalance": "白平衡",
            "shutterPlaceholder": "例如 1/200",
            "aperturePlaceholder": "例如 2.8",
            "isoPlaceholder": "例如 400",
            "autoOpenCaptured": "自动打开拍摄的照片",
            "capturing": "正在拍摄...",
            "triggerCapture": "触发拍摄",
            "toasts": {
                "noCamerasFound": "未找到相机。请确保处于 PC 遥控模式。",
                "detectionFailed": "检测失败: {{err}}",
                "communicationFailed": "与相机通信失败",
                "connectionFailed": "连接失败: {{err}}",
                "setFailed": "设置 {{key}} 失败: {{err}}",
                "selectFolderFirst": "请先在图库中选择一个普通文件夹。",
                "captureFailed": "拍摄失败: {{err}}",
                "cameraDisconnected": "相机已断开连接"
            }
        }
    },
    "zh-TW": {
        "editor": {
            "switcher": {
                "tooltips": {
                    "tethering": "連線拍攝"
                }
            }
        },
        "tethering": {
            "title": "連線拍攝",
            "scanTooltip": "掃描相機",
            "status": "狀態",
            "cameraConnected": "相機已連線",
            "selectCamera": "選擇相機",
            "startLiveView": "開啟即時取景",
            "stopLiveView": "停止即時取景",
            "noCameraDetected": "未偵測到相機",
            "liveViewAlt": "即時取景",
            "ghostOverlayAlt": "疊圖預覽",
            "overlayOff": "關閉",
            "rotate90": "旋轉 90°",
            "flipHorizontal": "水平翻轉",
            "overlayLastShot": "疊加上一張拍攝相片",
            "selectCameraPlaceholder": "選擇一台相機",
            "noCamerasFound": "未找到相機。請確保已連線並處於 PC 遙控模式。",
            "connectCamera": "連線相機",
            "exposureSettings": "曝光設定",
            "shutter": "快門",
            "aperture": "光圈",
            "iso": "ISO",
            "whiteBalance": "白平衡",
            "shutterPlaceholder": "例如 1/200",
            "aperturePlaceholder": "例如 2.8",
            "isoPlaceholder": "例如 400",
            "autoOpenCaptured": "自動開啟拍攝的影像",
            "capturing": "正在拍攝...",
            "triggerCapture": "觸發拍攝",
            "toasts": {
                "noCamerasFound": "未找到相機。請確保處於 PC 遙控模式。",
                "detectionFailed": "偵測失敗: {{err}}",
                "communicationFailed": "與相機通訊失敗",
                "connectionFailed": "連線失敗: {{err}}",
                "setFailed": "設定 {{key}} 失敗: {{err}}",
                "selectFolderFirst": "請先在媒體庫中選擇一個一般資料夾。",
                "captureFailed": "拍攝失敗: {{err}}",
                "cameraDisconnected": "相機已中斷連線"
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