from pathlib import Path

from constant.kind import kind_text, kind_voice, kind_photo
from infrastructure.ABC.I_adv_repo import IFileAdvRepo
import json

Path("data").mkdir(parents=True, exist_ok=True)

class FileAdvRepo(IFileAdvRepo):

    def __init__(self, data):
        self.user_id = data.get("user_id")
        self.type_avg = data.get("kind")
        self.caption = (data.get("caption") or "").strip()
        self.file_id = data.get("file_id")
        self.text = data.get("text")

    async def save_adv_data(self):
        user_id = {"user_id" : self.user_id}
        type_avg = {"type" : self.type_avg}
        content = {"content" : self.text}


        with open("data/ads.json", "w") as f:
            if self.type_avg == kind_text:
                data = user_id | type_avg | content
                json.dump(data, f, indent=2)




