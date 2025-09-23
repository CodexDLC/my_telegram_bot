# setting/config.py
import os
from dotenv import load_dotenv

# Эта команда загрузит переменные из .env файла,
# ТОЛЬКО если они еще не заданы в окружении (что идеально для Docker).
load_dotenv()



# Используем os.getenv(), это стандартный способ
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден. Проверьте .env файл или переменные окружения.")

# В вашем коде вы назвали переменную GPT_TOKEN, я сохранил это имя
GPT_TOKEN = os.getenv("OPENAI_TOKEN")
if not GPT_TOKEN:
    raise RuntimeError("OPENAI_TOKEN не найден. Проверьте .env файл или переменные окружения.")