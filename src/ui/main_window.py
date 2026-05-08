from datetime import date
from pathlib import Path
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QMessageBox)
from PySide6.QtCore import Slot
from src.ui.divider_maker import create_line
from src.ui.hospital_block import HospitalBlock
from src.ui.salemode_block import SalemodeBlock
from src.ui.product_block import ProductBlock
from src.models.excel_manager import ExcelManager
import data.config as config

class Mainwindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("制单系统")
        self.set_layout()
        self.connect_cross_signals()

    def set_layout(self):
        self.setFixedSize(600, 650)
        main_layout = QVBoxLayout(self)
        
        # 区块1:选择医院
        self.hosp_block = HospitalBlock()
        main_layout.addWidget(self.hosp_block)

        line_1 = create_line()
        main_layout.addWidget(line_1)

        # 区块2:选择出库选项
        self.salemode_block = SalemodeBlock()
        main_layout.addWidget(self.salemode_block)

        line_2 = create_line()
        main_layout.addWidget(line_2)

        # 区块3:添加产品
        self.product_block = ProductBlock()
        main_layout.addWidget(self.product_block)

        # 最终确认按钮，生成表格
        self.final_confirm = QPushButton("信息无误，确认制单")
        self.final_confirm.setFixedWidth(180)

        final_layout = QHBoxLayout()
        final_layout.addStretch()
        final_layout.addWidget(self.final_confirm)
        final_layout.addStretch()
        main_layout.addLayout(final_layout)

    def connect_cross_signals(self):
        self.final_confirm.clicked.connect(self.on_final_confirm_clicked)

    @Slot()
    def on_final_confirm_clicked(self):
        # 检查界面上数据完整性,若完整则获取,否则退出函数
        if not self.check_materials():
            return
        # 读入模板
        self.new_excel = self.create_excel()

        # 从界面读取表格表头信息放入字典
        self.header_dict = self.get_header()
        # 将字典写入文件头部信息
        self.new_excel.write_header(self.header_dict)

        # 写入产品信息
        self.new_excel.write_body(self.product_block.product_row_mapping)

        # 默认保存表格到桌面
        self.new_excel.save()
        
        
        # 获取body的写入位置
        # 将数据写入对应位置
        # 保存关闭文件

    def create_excel(self):
        return ExcelManager(Path(config.TEMPLETES_FPATH) / f"{self.hosp_block.hosp_combo.currentText()}模板.xlsx")
    
    def check_materials(self) -> bool:
        # 检查界面数据完整性
        if self.hosp_block.hosp_combo.currentIndex() == -1 or \
        not self.product_block.product_row_mapping:
            QMessageBox.information(self, "表格信息不完整", '请确认 "医院、商品" 信息完整！')
            return False
        return True
        
    def get_header(self) -> dict:
        temp_dict = {}
        
        # 将需要写入表格数据添加到字典
        temp_dict["hospital"] = f"收货单位：{self.hosp_block.hosp_holename_lbl.text()}"
        temp_dict["supplier"] = self.salemode_block.suppliers[self.salemode_block.suppliers_group.checkedButton().text()]
        temp_dict["salemode"] = self.salemode_block.salemodes_group.checkedButton().text() 
        temp_dict["ordermode"] = self.salemode_block.ordermodes_group.checkedButton().text() 
        temp_dict["orderdate"] = date.today()
        return temp_dict
    
    