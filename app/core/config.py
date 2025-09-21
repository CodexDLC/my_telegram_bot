# setting/config.py

from os import getenv
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в .env")

GPT_TOKEN = getenv("OPENAI_TOKEN")

if not GPT_TOKEN:
    raise RuntimeError("GPT_TOKEN не задан в .env")