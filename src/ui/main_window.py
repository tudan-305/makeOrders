from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Slot
from src.ui.divider_maker import create_line
from src.ui.hospital_block import HospitalBlock
from src.ui.salemode_block import SalemodeBlock
from src.ui.product_block import ProductBlock



class Mainwindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("制单系统")
        self.set_layout()
        self.connect_cross_signals()
    

    def set_layout(self):
        self.setFixedSize(700, 800)
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

        
        # 最终确认
        self.final_confirm = QPushButton("信息无误，确认制单")
        self.final_confirm.setFixedWidth(200)
        self.final_confirm.setStyleSheet("background-color:blue;foreground-color:white")
        final_layout = QHBoxLayout(self)
        final_layout.addStretch()
        final_layout.addWidget(self.final_confirm)
        final_layout.addStretch()
        main_layout.addLayout(final_layout)
    def connect_cross_signals(self):
        pass
    
    @Slot()
    def on_hosp_selected(self, text):
        print(f"全名是：{text}")
    


