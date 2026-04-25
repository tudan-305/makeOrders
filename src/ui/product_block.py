from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,QPushButton, QLabel, QLineEdit,
    QComboBox, QRadioButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QSpinBox)
from PySide6.QtCore import Signal, Slot, Qt
from src.models.product import Product

#区块3制作
class ProductBlock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
        # 存储产品名称与行号的映射，方便快速查找
        self.product_row_mapping = {}

    def setup_ui(self):
        # 顶部：扫码输入框(带说明) + 手动添加按钮
        input_layout = QHBoxLayout()
        self.scan_input = QLineEdit()
        self.scan_input.setPlaceholderText("扫入商品二维码")
        self.add_btn = QPushButton("添加")
        input_layout.addWidget(self.scan_input)
        input_layout.addWidget(self.add_btn)

        # 中间：产品显示表格
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['产品名称', 'UDI码', '批号/序列号', '数量'])
        # 第一列填满界面
        # 1,2,3,4列：名称，udi，批号/序列号，数量
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        # self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        # 底部：删除选中行按钮
        self.delete_btn = QPushButton("删除选中商品")
        
        layout = QVBoxLayout(self)
        layout.addLayout(input_layout)
        layout.addWidget(self.table)
        layout.addWidget(self.delete_btn)

    def connect_signals(self):
        self.scan_input.returnPressed.connect(self.add_product_from_scan)
        self.add_btn.clicked.connect(self.add_product_from_scan)
        self.delete_btn.clicked.connect(self.delete_selected_product)

    @Slot()
    def add_product_from_scan(self):
        try:
            # 判断输入是否只有空白字符
            product_udi = self.scan_input.text().strip()
            if not product_udi:
                return
            
            # 检查新添加是否已存在
            if product_udi in self.product_row_mapping:
                # 获取产品行号（字典格式为{"udi":["产品实例", "行号"]}
                row = self.product_row_mapping[product_udi][1]
                # 获取当前数量控件的值并增加1
                spin_box = self.table.cellWidget(row, 3)
                # 若有这个控件，数量+1
                if spin_box:
                    new_quantity = spin_box.value() + 1
                    spin_box.setValue(new_quantity)
            else:
                # 添加产品,判断是否有效GS1码
                new_product = Product(product_udi)
                if not new_product.is_gs1:
                    QMessageBox.warning(self, "无效条码", "无效的产品GS1码，请重新扫入")
                    return
                
                # 添加新行
                row = self.table.rowCount()
                self.table.insertRow(row)

                column1_text = f"{new_product.model_No:<18}{new_product.name}"
                column2_text = f"{product_udi}"
                column3_text = f"{new_product.serial_number if new_product.serial_number else new_product.batch_number}"
                # 设置悬停显示文本
                new_item1 = QTableWidgetItem(column1_text)
                new_item1.setToolTip(column1_text)
                new_item2 = QTableWidgetItem(column2_text)
                new_item2.setToolTip(column2_text)
                new_item3 = QTableWidgetItem(column3_text)
                # 设置单元格为不可编辑
                # flags()一个整数，一些初始设置标志位默认为1， Qt.ItemIsEditable 二进制值为10
                # 按位取反以后，为11111101，与远设置按位与，得到是否可编辑位上为0, 其他位值不变
                new_item1.setFlags(new_item1.flags() & ~Qt.ItemIsEditable)
                new_item2.setFlags(new_item2.flags() & ~Qt.ItemIsEditable)
                new_item3.setFlags(new_item3.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 0, new_item1)
                self.table.setItem(row, 1, new_item2)
                self.table.setItem(row, 2, new_item3)

                #数量控件：添加QSpinBox作为单元格控件
                spin_box = QSpinBox()
                spin_box.setMinimum(1)
                spin_box.setMaximum(99999)
                spin_box.setValue(1)
                # 数量改变时，触发后续逻辑，比如重新计算总价格
                spin_box.valueChanged.connect(lambda value, r=row: self.on_quantity_changed(value, r))

                # 添加部件
                self.table.setCellWidget(row, 3, spin_box)
                # 记录映射
                self.product_row_mapping[product_udi] = [new_product, row]
        finally: 
            # 清空输入框，准备下次输入
            self.scan_input.clear()

    @Slot()
    def on_quantity_changed(self, new_value, row):
        pass

    @Slot()
    def delete_selected_product(self):
        pass

    def refresh_row_mapping(self):
        pass
