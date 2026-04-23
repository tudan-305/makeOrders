import biip
from data.config import DEVICES_TABLE

class Product:
    def __init__(self, gs1_code: str):
        self.gs1_code = gs1_code
        self.parse()

    def parse(self):
        parsed_gs1 = biip.parse(self.gs1_code).gs1_message
        parsed_res = parsed_gs1.element_strings
        data = {el.ai.ai:el.value for el in parsed_res}
        self.udi           = parsed_gs1.as_hri()                                     # 产品UDI码
        self.gtin          = data.get("01")                                          # GTIN
        self.name          = DEVICES_TABLE.at[self.gtin, "产品名称/通用名称"]          # 产品名称    
        self.model_No      = DEVICES_TABLE.at[self.gtin, "规格型号"]                  # 规格型号
        self.reg_No        = DEVICES_TABLE.at[self.gtin, "注册证编号或者备案凭证编号"]   # 注册证号
        self.batch_number  = data.get("10")                                         # 批号
        self.serial_number = data.get("21")                                         # 序列号
        self.expiry        = data.get("17")                                         # 失效日期
        self.prod_date     = data.get("11")                                         # 生产日期
        self.quantity      = 1                                                      # 数量
        self.unit          = None                                                   # 单位
        self.unit_price    = DEVICES_TABLE.at[self.gtin, "单价"]                     # 单价
        self.amout         = 0                                                      # 总价

# new = Product("0100380652250535172903102115820772080\x1d11240312240SN6AT4255")
# print(new.reg_No)
# print(type(new.udi))