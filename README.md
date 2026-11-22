<div align="center">

~~~text
██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗
██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝
██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║
██╔══██╗██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║
██████╔╝██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║
╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝
~~~

**// BOOKPDF-TO-SOUND · PROJECT README**

*source · setup · architecture · security*

[![README style](https://img.shields.io/badge/README-Codex%20Style-00D9FF?style=for-the-badge)](https://github.com/Bifyp/codex-agent-workbench)

</div>

---

## > PROJECT.STATUS

| FIELD | VALUE |
|:--|:--|
| Repository | Bifyp/bookpdf-to-sound |
| Documentation | Russian README + English README.en.md |
| Secrets | Never commit tokens, keys, sessions, or .env files |

## > PROJECT.DOCUMENTATION

<div align="center">

```
██████╗  ██████╗  ██████╗ ██╗  ██╗    ████████╗ ██████╗ 
██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝    ╚══██╔══╝██╔═══██╗
██████╔╝██║   ██║██║   ██║█████╔╝        ██║   ██║   ██║
██╔══██╗██║   ██║██║   ██║██╔═██╗        ██║   ██║   ██║
██████╔╝╚██████╔╝╚██████╔╝██║  ██╗       ██║   ╚██████╔╝
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝       ╚═╝    ╚═════╝ 

███████╗██████╗ ███████╗███████╗ ██████╗██╗  ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝██║  ██║
███████╗██████╔╝█████╗  █████╗  ██║     ███████║
╚════██║██╔═══╝ ██╔══╝  ██╔══╝  ██║     ██╔══██║
███████║██║     ███████╗███████╗╚██████╗██║  ██║
╚══════╝╚═╝     ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝
```

**`// BOOK TO SPEECH v1.0`**

*PDF → MP3 · по главам · Edge TTS · без GPU · бесплатно*

---

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Edge TTS](https://img.shields.io/badge/TTS-edge--tts-FF007A?style=for-the-badge)](https://github.com/rany2/edge-tts)
[![pdfplumber](https://img.shields.io/badge/PDF-pdfplumber-orange?style=for-the-badge)](https://github.com/jsvine/pdfplumber)
[![License](https://img.shields.io/badge/License-MIT-00FFCC?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)](https://github.com)

</div>

---

```
  ╔══════════════════════════════════════════════════════════════════════╗
  ║                                                                      ║
  ║   INPUT                    ENGINE                OUTPUT              ║
  ║   ─────                    ──────                ──────              ║
  ║   book.pdf  ──━━━━━━━━━━►  pdfplumber             audio_chapters/    ║
  ║                            ├── text extract       ├── Глава_01.mp3   ║
  ║                            └── chapter split      ├── Глава_02.mp3   ║
  ║                                    │              └── ...            ║
  ║                                    ▼                                 ║
  ║                            edge-tts (Microsoft)                      ║
  ║                            ├── ru-RU-DmitryNeural                    ║
  ║                            ├── ru-RU-SvetlanaNeural                  ║
  ║                            └── ru-RU-DariyaNeural                    ║
  ║                                                                      ║
  ║   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░     ║
  ║   STATUS: // FREE   ▌  NO GPU REQUIRED   ▌  ASYNC ENGINE             ║
  ╚══════════════════════════════════════════════════════════════════════╝
```

---

## `> SYSTEM.FEATURES`

| МОДУЛЬ | ОПИСАНИЕ | СТАТУС |
|:-------|:---------|:------:|
| `PDF_READER` | Извлечение текста постранично через pdfplumber | `[ACTIVE]` |
| `CHAPTER_SPLIT` | Авторазбивка на главы по маркерам `# ГЛАВА N` | `[ACTIVE]` |
| `TTS_ENGINE` | Синтез речи Microsoft Edge TTS — без API-ключей | `[ACTIVE]` |
| `VOICE_SELECT` | 3 русских голоса: Dmitry · Svetlana · Dariya | `[ACTIVE]` |
| `RESUME_MODE` | Пропуск уже готовых глав при повторном запуске | `[ACTIVE]` |
| `PROGRESS_BAR` | Прогресс-бар + прогноз времени в консоли | `[ACTIVE]` |
| `ERROR_RETRY` | Авто-повтор при сбое TTS-запроса | `[ACTIVE]` |
| `RANGE_MODE` | Озвучка только выбранного диапазона глав | `[ACTIVE]` |

---

## `> QUICK.BOOT`

### Требования

```
Runtime   ─── Python 3.10+
Platform  ─── Windows / Linux / macOS
Network   ─── Интернет (Edge TTS работает онлайн)
```

### `// STEP 1 — клонирование`

```bash
git clone https://github.com/your_username/book-to-speech.git
cd book-to-speech
```

### `// STEP 2 — зависимости`

```bash
pip install -r requirements.txt
```

### `// STEP 3 — подготовка`

Положите PDF-книгу рядом со скриптом и укажите путь в настройках:

```python
# book_to_speech_edge.py — секция НАСТРОЙКИ
PDF_PATH   = "Ваша_книга.pdf"
OUTPUT_DIR = "audio_chapters"
```

### `// STEP 4 — запуск`

```bash
python book_to_speech_edge.py
```

---

## `> CONFIG.TABLE`

```
╔══════════════════════╦═══════════════════════════════════════════════╗
║   ПАРАМЕТР           ║   ОПИСАНИЕ                                    ║
╠══════════════════════╬═══════════════════════════════════════════════╣
║  PDF_PATH            ║  Путь к PDF-файлу                             ║
║  OUTPUT_DIR          ║  Папка для MP3-файлов (создаётся авто)        ║
╠══════════════════════╬═══════════════════════════════════════════════╣
║  VOICE               ║  Голос Edge TTS (см. таблицу голосов ниже)    ║
║  RATE                ║  Скорость речи: "+0%" / "+10%" / "-10%"       ║
╠══════════════════════╬═══════════════════════════════════════════════╣
║  CHAPTER_FROM        ║  Начальная глава (None = с первой)            ║
║  CHAPTER_TO          ║  Конечная глава  (None = до последней)        ║
╚══════════════════════╩═══════════════════════════════════════════════╝
```

### Голоса

```
┌──────────────────────────────┬──────────────────────────────────────┐
│   VOICE                      │   ОПИСАНИЕ                           │
├──────────────────────────────┼──────────────────────────────────────┤
│  ru-RU-DmitryNeural          │  Мужской, чёткий          (рекоменд) │
│  ru-RU-SvetlanaNeural        │  Женский, мягкий                     │
│  ru-RU-DariyaNeural          │  Женский, живой                      │
└──────────────────────────────┴──────────────────────────────────────┘
```

---

## `> FORMAT.PROTOCOL`

Скрипт ищет главы по паттерну:

```
# ГЛАВА 1 НАЗВАНИЕ
# ГЛАВА 2 ДРУГОЕ_НАЗВАНИЕ
```

Убедитесь, что в вашем PDF главы отмечены именно так.  
Паттерн можно изменить в функции `split_into_chapters()`.

---

## `> OUTPUT.STRUCTURE`

```
book-to-speech/
│
├── book_to_speech_edge.py     основной скрипт
├── requirements.txt           зависимости
├── .gitignore
│
└── audio_chapters/            ← создаётся автоматически
    ├── Глава_01_НАЗВАНИЕ.mp3
    ├── Глава_02_НАЗВАНИЕ.mp3
    └── ...
```

---

## `> CONSOLE.OUTPUT`

```
═══════════════════════════════════════════════════════
  ОЗВУЧКА КНИГИ — Ваша книга
  Голос: ru-RU-DmitryNeural  |  Скорость: +0%
═══════════════════════════════════════════════════════

───────────────────────────────────────────────────────
 ШАГ 1: Чтение PDF
───────────────────────────────────────────────────────
  Файл: book.pdf
  Страниц в книге: 312
  [████████████████████] 100%  (312/312 стр.)
  ✓ PDF прочитан за 0м 8с

 ШАГ 2: Разбивка на главы
───────────────────────────────────────────────────────
  ✓ Найдено глав: 24

 ШАГ 3: Синтез речи
───────────────────────────────────────────────────────
  [1/24] Глава 1 — НАЗВАНИЕ
  Символов в главе:  8,450
  Статус:            ✓ Готово!
  Общий прогресс:    [█░░░░░░░░░░░░░░░░░░░] 4%  (1/24)
```

---

<div align="center">

```
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 ░                                                    ░
 ░         // YOUR BOOK.  YOUR VOICE.  FREE.          ░
 ░               BOOK TO SPEECH v1.0                  ░
 ░                                                    ░
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

</div>
