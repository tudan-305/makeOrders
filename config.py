# 此文件存放文件地址,全局变量
import sys
from pathlib import Path

# 数据地址

def get_root_path():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    else:
        return Path(__file__).resolve().parent
    
ROOT_PATH = get_root_path()
DESKTOP = Path().home() / "Desktop"
PRODUCT_DATA_FPATH = ROOT_PATH / "data/udid_devices_alcon.csv"
HOSP_JSON_FPATH = ROOT_PATH / "data/hospital_names.json"
TEMPLATES_FPATH = ROOT_PATH / "templates"


