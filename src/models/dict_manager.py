import json
from pathlib import Path
from pypinyin import lazy_pinyin
#医院字典文件地址
hosp_json = "data/hospital_names.json"
hosp_init ={
            "温眼": "温州医科大学附属眼视光医院杭州院区",
            "浙二": "浙大二院眼科中心浙江大学眼科医院",
            "浙一庆春": "浙江大学医学院附属第一医院(庆春院区)",
        }

class DictManager:
    def __init__(self, file_path:str, init_mapping:dict, parent=None):
        super().__init__(parent)
        self.file_path = Path(file_path)
        self.init_mapping = init_mapping
        self.dict = self.load()
        self.dict = self.rank()

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            with open(self.init_mapping, "w", encoding="utf-8") as f:
                json.dump(self.dict, f, ensure_ascii=False, indent=4)
                return self.init_mapping
    
    def rank(self):
        self.dict = dict(sorted(self.dict.items(), key = lambda x: x[0]))

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
    
hosp_mapping = DictManager(hosp_json, hosp_init)
