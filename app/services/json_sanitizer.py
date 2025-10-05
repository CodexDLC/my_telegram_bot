# app/services/json_sanitizer.py (или прямо в quiz_service.py)
import json
import re

def extract_json_str(s: str) -> str:
    """Возвращает строку с валидным JSON (объект или массив) из произвольного ответа модели."""
    s = (s or "").strip()

    # 1) быстрый путь: вдруг уже чистый JSON
    try:
        json.loads(s)
        return s
    except Exception:
        pass

    # 2) markdown-кодблок ```json ... ``` или просто ```.
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", s, re.IGNORECASE)
    if m:
        inner = m.group(1).strip()
        try:
            json.loads(inner)
            return inner
        except Exception:
            s = inner  # пробуем разобрать ниже как "сырой" текст

    # 3) вырезать первый сбалансированный {..} или [..]
    start, open_ch, close_ch = None, None, None
    for i, ch in enumerate(s):
        if ch in "{[":
            start = i
            open_ch = ch
            close_ch = "}" if ch == "{" else "]"
            break

    if start is not None:
        depth = 0
        in_str = False
        esc = False
        for j in range(start, len(s)):
            ch = s[j]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
            else:
                if ch == '"':
                    in_str = True
                elif ch == open_ch:
                    depth += 1
                elif ch == close_ch:
                    depth -= 1
                    if depth == 0:
                        candidate = s[start:j+1].strip()
                        # финальная проверка
                        json.loads(candidate)
                        return candidate

    raise ValueError("Не удалось извлечь валидный JSON из ответа модели.")
