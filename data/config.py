# 此文件存放文件地址,全局变量
import pandas as pd

# 数据地址
PRODUCT_DATA_FPATH = "data/udid_devices_alcon.csv"
HOSP_JSON_FPATH = "data/hospital_names.json"

# 读入爱尔康产品数据表
DEVICES_TABLE = pd.read_csv(PRODUCT_DATA_FPATH, index_col="最小销售单元产品标识",
                            header=0,           dtype={"最小销售单元产品标识":str}
                            )
