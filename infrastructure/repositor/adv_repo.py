from pathlib import Path

from constant.kind import kind_text, kind_voice, kind_photo
from infrastructure.ABC.I_adv_repo import IFileAdvRepo
import json

ADS_PATH = Path("data/ads.json")
ADS_PATH.parent.mkdir(parents=True, exist_ok=True)

class FileAdvRepo(IFileAdvRepo):
    def __init__(self, data):
        self.user_id = data.get("user_id")
        self.type_avg = data.get("kind")
        self.caption = (data.get("caption") or "").strip()
        self.file_id = data.get("file_id")
        self.text = data.get("text")

    async def save_adv_data(self):
        entry = {"user_id": self.user_id, "type": self.type_avg}

        if self.type_avg == kind_text:
            entry["content"] = self.text
        elif self.type_avg == kind_photo:
            entry["file_id"] = self.file_id
            entry["caption"] = self.caption
        elif self.type_avg == kind_voice:
            entry["file_id"] = self.file_id
        else:
            return  # неизвестный тип — ничего не пишем

        # TODO likes пока не реализован
        # entry["likes"] = 0

        items = []
        if ADS_PATH.exists():
            try:
                with ADS_PATH.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    items = data if isinstance(data, list) else [data]
            except json.JSONDecodeError:
                items = []

        items.append(entry)

        tmp = ADS_PATH.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        tmp.replace(ADS_PATH)