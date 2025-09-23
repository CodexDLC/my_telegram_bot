# setting/config.py
import os
from os import getenv
from dotenv import load_dotenv


load_dotenv()

def _clean(s: str) -> str:
    return s.strip().strip('"').strip("'") if s else s

BOT_TOKEN = _clean(os.getenv("BOT_TOKEN"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в .env")

GPT_TOKEN = getenv("OPENAI_TOKEN")

if not GPT_TOKEN:
    raise RuntimeError("GPT_TOKEN не задан в .env")