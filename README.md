# 项目名称：眼科器械出库表格生成工具

### 1.项目环境
确保你的电脑安装python3.12 或更高版本

### 2.项目依赖
创建venv环境后，在终端内运行 python install -r requirements.txt

### 3.项目运行
根目录下，执行python main.py

### 3.项目结构
data/config.py 存放文件地址等信息
data/hospital_nams.json 存放医院名称映射
data/udid_devices_alcon.csv 存放爱尔康产品信息

src/models 存放字典管理，excel管理等组件
src/ui 存放应用界面

templetes/ 存放excel模板

tests/ 一些测试功能

### 4.注意事项
生成表格如果数据有误首先去data/的udid_devices_alcon.csv 里面修改

### 5.其他
医院排序的时候用到了 pypinyin 库来根据拼音排序


