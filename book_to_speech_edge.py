"""
Озвучка книги "Проект Красный снег" по главам с помощью Edge TTS
Бесплатно, работает на Python 3.14, не нужен GPU.

Установка:
    pip install edge-tts pdfplumber

Использование:
    python book_to_speech_edge.py

Результат:
    Папка audio_chapters/ с файлами:
    Глава_01_УТЕЧКА.mp3, Глава_02_НИЖНИЙ_ГОРОД.mp3, ...
"""

import re
import os
import asyncio
import time
import pdfplumber
import edge_tts
from pathlib import Path

# ─────────────────────────────────────────────
# НАСТРОЙКИ
# ─────────────────────────────────────────────

PDF_PATH   = "Проект Красный снег.pdf"
OUTPUT_DIR = "audio_chapters"

# Голоса:
#   ru-RU-DmitryNeural   — мужской, чёткий (рекомендую)
#   ru-RU-SvetlanaNeural — женский, мягкий
#   ru-RU-DariyaNeural   — женский, живее
VOICE = "ru-RU-DmitryNeural"

# Скорость: "+0%" = норма, "+10%" = быстрее, "-10%" = медленнее
RATE = "+0%"

# Диапазон глав (None = все)
CHAPTER_FROM = None
CHAPTER_TO   = None

# ─────────────────────────────────────────────

def log(msg, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{msg}")

def format_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h}ч {m}м {s}с"
    return f"{m}м {s}с"

def format_size(path: str) -> str:
    size = os.path.getsize(path)
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} КБ"
    return f"{size / 1024 / 1024:.1f} МБ"

def print_separator(char="─", width=55):
    print(char * width)

def print_header():
    print_separator("═")
    log("  ОЗВУЧКА КНИГИ — Проект Красный снег")
    log(f"  Голос: {VOICE}  |  Скорость: {RATE}")
    print_separator("═")
    print()


def extract_text_from_pdf(pdf_path: str) -> str:
    print_separator()
    log("📄 ШАГ 1: Чтение PDF")
    print_separator()
    log(f"Файл: {pdf_path}", 1)

    parts = []
    t0 = time.time()
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        log(f"Страниц в книге: {total}", 1)
        log("Извлекаю текст...", 1)
        for i, page in enumerate(pdf.pages):
            t = page.extract_text()
            if t:
                parts.append(t)
            if (i + 1) % 100 == 0:
                pct = (i + 1) / total * 100
                log(f"[{'█' * int(pct // 5):<20}] {pct:.0f}%  ({i+1}/{total} стр.)", 1)

    elapsed = time.time() - t0
    full_text = "\n".join(parts)
    log(f"[{'█' * 20}] 100%  ({total}/{total} стр.)", 1)
    log(f"✓ PDF прочитан за {format_time(elapsed)}", 1)
    log(f"  Всего символов: {len(full_text):,}", 1)
    print()
    return full_text


def split_into_chapters(full_text: str) -> list:
    print_separator()
    log("📑 ШАГ 2: Разбивка на главы")
    print_separator()
    log("Ищу маркеры глав...", 1)

    pattern = re.compile(r"^# ГЛАВА (\d+)\s*(.*?)$", re.MULTILINE)
    matches = list(pattern.finditer(full_text))
    if not matches:
        raise ValueError("Главы не найдены.")

    chapters = []
    for i, match in enumerate(matches):
        num   = int(match.group(1))
        title = match.group(2).strip() or f"Глава {num}"
        start = match.end()
        end   = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        text  = clean_chapter_text(full_text[start:end].strip())
        chapters.append({"num": num, "title": title, "text": text})

    log(f"✓ Найдено глав: {len(chapters)}", 1)
    total_chars = sum(len(c["text"]) for c in chapters)
    log(f"  Суммарно символов: {total_chars:,}", 1)
    avg = total_chars // len(chapters)
    log(f"  Средний размер главы: {avg:,} символов", 1)
    print()
    return chapters


def clean_chapter_text(text: str) -> str:
    lines, cleaned = text.splitlines(), []
    for line in lines:
        line = line.strip()
        if not line:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue
        if re.fullmatch(r"\d{1,4}", line):
            continue
        if re.match(r"^Глава\s+\d+", line, re.IGNORECASE):
            continue
        if re.match(r"^#\s*ATK\s+\d+", line):
            continue
        if line == "Без названия":
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()


async def synthesize_chapter(text: str, out_path: str):
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(out_path)


def safe_filename(num: int, title: str) -> str:
    clean = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")[:50]
    return f"Глава_{num:02d}_{clean}.mp3"


async def main():
    print_header()

    if not os.path.exists(PDF_PATH):
        log(f"✗ Файл не найден: {PDF_PATH}")
        log("  Положите PDF рядом со скриптом.")
        return

    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    full_text = extract_text_from_pdf(PDF_PATH)
    chapters  = split_into_chapters(full_text)

    if CHAPTER_FROM or CHAPTER_TO:
        lo = CHAPTER_FROM or 1
        hi = CHAPTER_TO or 9999
        chapters = [c for c in chapters if lo <= c["num"] <= hi]

    # Пропускаем уже готовые
    already_done = []
    to_process   = []
    for ch in chapters:
        path = os.path.join(OUTPUT_DIR, safe_filename(ch["num"], ch["title"]))
        if os.path.exists(path):
            already_done.append(ch)
        else:
            to_process.append(ch)

    print_separator()
    log("🎙 ШАГ 3: Синтез речи")
    print_separator()
    log(f"Всего глав:      {len(chapters)}", 1)
    log(f"Уже готово:      {len(already_done)}", 1)
    log(f"Нужно озвучить:  {len(to_process)}", 1)
    log(f"Папка вывода:    {OUTPUT_DIR}/", 1)
    print()

    if not to_process:
        log("✓ Все главы уже озвучены!")
        return

    total_start = time.time()
    chapter_times = []

    for idx, ch in enumerate(to_process):
        filename = safe_filename(ch["num"], ch["title"])
        out_path = os.path.join(OUTPUT_DIR, filename)
        chars    = len(ch["text"])

        print_separator("─")
        log(f"[{idx+1}/{len(to_process)}] Глава {ch['num']} — {ch['title']}")
        print_separator("─")
        log(f"Символов в главе:  {chars:,}", 1)
        log(f"Файл:              {filename}", 1)
        log(f"Статус:            ⏳ Отправляю запрос к Edge TTS...", 1)

        t0 = time.time()
        try:
            await synthesize_chapter(ch["text"], out_path)
        except Exception as e:
            log(f"Статус:            ✗ Ошибка: {e}", 1)
            log("                   🔄 Повтор через 3 секунды...", 1)
            await asyncio.sleep(3)
            try:
                await synthesize_chapter(ch["text"], out_path)
            except Exception as e2:
                log(f"Статус:            ✗ Повтор не помог: {e2}", 1)
                log("                   ⚠ Глава пропущена", 1)
                print()
                continue

        elapsed = time.time() - t0
        chapter_times.append(elapsed)

        # Размер файла
        size_str = format_size(out_path)

        # Среднее время и прогноз
        avg_time  = sum(chapter_times) / len(chapter_times)
        remaining = avg_time * (len(to_process) - (idx + 1))
        total_elapsed = time.time() - total_start

        log(f"Статус:            ✓ Готово!", 1)
        log(f"Время синтеза:     {format_time(elapsed)}", 1)
        log(f"Размер файла:      {size_str}", 1)
        log(f"Прошло всего:      {format_time(total_elapsed)}", 1)
        log(f"Осталось примерно: {format_time(remaining)}", 1)

        done_count = len(already_done) + idx + 1
        total_count = len(chapters)
        pct = done_count / total_count * 100
        bar = '█' * int(pct // 5)
        log(f"Общий прогресс:    [{bar:<20}] {pct:.0f}%  ({done_count}/{total_count})", 1)
        print()

    # Итог
    print_separator("═")
    log("  ГОТОВО!")
    print_separator("═")
    total_elapsed = time.time() - total_start
    log(f"Озвучено глав:  {len(to_process)}", 1)
    log(f"Затрачено:      {format_time(total_elapsed)}", 1)
    log(f"Файлы в папке:  {OUTPUT_DIR}/", 1)

    # Общий размер папки
    total_size = sum(
        os.path.getsize(os.path.join(OUTPUT_DIR, f))
        for f in os.listdir(OUTPUT_DIR)
        if f.endswith(".mp3")
    )
    log(f"Всего аудио:    {total_size / 1024 / 1024:.1f} МБ", 1)
    print_separator("═")


if __name__ == "__main__":
    asyncio.run(main())