from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QLineEdit, QComboBox, 
                               QRadioButton, QTableWidget, QTableWidgetItem,
                               QHeaderView, QSpinBox)
from PySide6.QtCore import Signal, Slot
from src.models.product import Product

#区块3制作
class ProductBlock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
        # 存储产品名称与行号的映射，方便快速查找
        self.product_row_map = {}

    def setup_ui(self):
        # 顶部：扫码输入框(带说明) + 手动添加按钮
        input_layout = QHBoxLayout()
        self.scan_input = QLineEdit()
        self.scan_input.setPlaceholderText("扫入商品二维码/键盘手动输入")
        self.add_btn = QPushButton("手动添加")
        self.add_btn.clicked.connect(self.add_product_from_scan)
        input_layout.addWidget(self.scan_input)
        input_layout.addWidget(self.add_btn)

        # 中间：产品显示表格
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(['产品名称', '数量'])
        # 第一列填满界面，第二列按内容自适应宽度
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # 启用编辑（数量列使用自定义控件）
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | 
                                   QTableWidget.EditTrigger.EditKeyPressed)
        
        # 底部：删除选中行按钮
        self.delete_btn = QPushButton("删除选中商品")
        
        layout = QVBoxLayout(self)
        layout.addLayout(input_layout)
        layout.addWidget(self.table)
        layout.addWidget(self.delete_btn)

    def connect_signals(self):
        self.scan_input.returnPressed.connect(self.add_product_from_scan)
        self.delete_btn.clicked.connect(self.delete_selected_product)

    @Slot()
    def add_product_from_scan(self):
        pass
    @Slot()
    def delete_selected_product(self):
        pass