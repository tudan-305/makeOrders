from openpyxl import load_workbook
from pathlib import Path
from data.config import TEMPLETES_FPATH

_excel_insert_position = {
    "温眼":{
        "发货单位": "B1",
        "发货日期": "E4",
        "收货单位": "A5",
        "销售模式": "K3",
        "商品名称": "A9",
        "商品规格": "B9",
        "生产企业": "C9",
        "注册证号": "D9",
        "序列号":  "E9",
        "生产日期": "F9",
        "有效期":  "G9",
        "数量":   "H9",
        "单位": "I9",
        "储存条件": "J9",
        "单价": "K9",
        "金额": "L9"
    },
    "浙一庆春":{

    }
}
class sheet_materials:
    def __init__(self, nick_name:str):
        order_templetes_path = Path(TEMPLETES_FPATH) / nick_name
        gift_templets_path = Path(TEMPLETES_FPATH) / (nick_name + "-赠品")
        insert_position = _excel_insert_position[nick_name]