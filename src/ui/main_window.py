from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Slot
from src.ui.divider_maker import create_line
from src.ui.hospital_block import HospitalBlock
from src.ui.salemode_block import SalemodeBlock
# from src.ui.product_block import ProductBlcok



class Mainwindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("制单系统")
        self.set_layout()
        self.connect_cross_signals()
    

    def set_layout(self):
        # self.setFixedSize(400, 200)
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

        # # 区块3:输入udi
        # layout_3rd = ProductBlcok()
        # main_layout.addLayout(layout_3rd)

    def connect_cross_signals(self):
        pass
    
    @Slot()
    def on_hosp_selected(self, text):
        print(f"全名是：{text}")
    


