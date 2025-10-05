# app/core/config.py
import os

from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN не найден. Проверьте .env файл или переменные окружения."
    )


GPT_TOKEN = os.getenv("OPENAI_TOKEN")
if not GPT_TOKEN:
    raise RuntimeError(
        "OPENAI_TOKEN не найден. Проверьте .env файл или переменные окружения."
    )

GEMINI_TOKEN = os.getenv("GEMINI_TOKEN")
if not GEMINI_TOKEN:
    raise RuntimeError(
        "GEMINI_TOKEN не найден. Проверьте .env файл или переменные окружения."
    )