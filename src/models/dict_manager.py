import json
from pathlib import Path
from pypinyin import lazy_pinyin
import data.config as config

class DictManager:
    def __init__(self, file_path:str):
        super().__init__()
        self.file_path = Path(file_path)
        self.dict = self.load()
        self.rank()
        self.save()

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
                return {}
    
    def rank(self):
        self.dict = dict(sorted(self.dict.items(), key = lambda item: item[0]))
                    
    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.dict, f, ensure_ascii=False, indent=4)

    def add(self, key:str, value:str):
        if key in self.dict:
            return False
        else:
            self.dict[key] = value
            return True
    
    def delete(self, key:str) -> bool:
        if key not in self.dict:
            return False
        del self.dict[key]
        self.save()
        return True
    
    def get_keys(self):
        return self.dict.keys()
    
    def get_value(self, key:str) -> str:
        return self.dict.get(key, "")
    
hosp_mapping = DictManager(config.HOSP_JSON_FPATH)
