from decimal import Decimal
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
        self.product_row_mapping = {} # 字典格式为{"udi":["产品实例", "行号"]}

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
        # 底部1：总数，总金额
        self.amount = Decimal("0.0")
        self.count = 0
        self.count_label = QLabel(f"总数: {self.count}")
        self.amount_label = QLabel(f"总金额: {self.amount}")
        layout_h1 = QHBoxLayout()
        layout_h1.addWidget(self.count_label)
        layout_h1.addWidget(self.amount_label)
        layout_h1.addStretch()
        # 底部2:删除选中行按钮
        self.delete_btn = QPushButton("删除选中商品")
        
        layout = QVBoxLayout(self)
        layout.addLayout(input_layout)
        layout.addWidget(self.table)
        layout.addLayout(layout_h1)
        layout.addWidget(self.delete_btn)

    def connect_signals(self):
        self.scan_input.returnPressed.connect(self.add_product_from_scan)
        self.add_btn.clicked.connect(self.add_product_from_scan)
        self.delete_btn.clicked.connect(self.delete_selected_product)
        self.table.model().rowsRemoved.connect(self.refresh_amount)

    @Slot()
    def add_product_from_scan(self):
        try:
            # 判断输入是否只有空白字符
            product_udi = self.scan_input.text().strip()
            if not product_udi:
                return
            
            # 检查新添加是否已存在
            if product_udi in self.product_row_mapping:
                # 获取产品行号  字典格式为{"udi":["产品实例", "行号"]}
                row = self.product_row_mapping[product_udi][1]
                # 获取当前数量控件的值并增加1
                spin_box = self.table.cellWidget(row-1, 3)
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
                # 设置单元格，并且悬停显示文本
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
                #设定任意不为1的初始值，下面重设一次数量触发信号，更新数量显示
                spin_box.setValue(99999)
                # 添加到字典，记录产品、行号映射
                self.product_row_mapping[product_udi] = [new_product, row+1]
                # 数量改变时，触发后续逻辑，如重新计算数量，价格
                spin_box.valueChanged.connect(lambda value, udi=product_udi:(print(f"lambda fired:{value}, {udi}"),self.on_quantity_changed(value, udi)))
                spin_box.valueChanged.connect(self.refresh_amount)
                spin_box.setValue(1)
                # 部件放入单元格
                self.table.setCellWidget(row, 3, spin_box)
                      
        finally:
            # 清空输入框，准备下次输入
            self.scan_input.clear()

    @Slot()
    def on_quantity_changed(self, new_quantity, udi):
        self.product_row_mapping[udi][0].quantity = new_quantity
        self.product_row_mapping[udi][0].refresh_amount()

    @Slot()
    def delete_selected_product(self):
        """删除当前产品行"""

        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "提示", "请先选中要删除产品行")
            return
        
        product_message = self.table.item(current_row, 0).text() + "\n" + \
                          "批号/序列号：" + self.table.item(current_row, 2).text()
        product_udi = self.table.item(current_row, 1).text()

        reply = QMessageBox.question(self, "确认删除", f"是否删除产品：\n'{product_message}'",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply != QMessageBox.Yes:
            return
        
        # 移除字典项
        del self.product_row_mapping[product_udi]
        # 刷新字典内记录的行号
        self._refresh_row_mapping(current_row)
        # 移除表格行
        self.table.removeRow(current_row)

    def _refresh_row_mapping(self, row):
        """遍历product_row_mapping, 将所有比删除行大的行都减1"""
        for key, (_, n) in self.product_row_mapping.items():
            if n > row:
                self.product_row_mapping[key][1] -= 1

    @Slot()
    def refresh_amount(self):
        self.amount = Decimal("0.0")
        self.count = 0
        for value in self.product_row_mapping.values():
            self.amount += value[0].amount
            self.count += value[0].quantity
        print(self.count)
        self.count_label.setText(f"总数：{self.count}")
        self.amount_label.setText(f"总金额：{self.amount}")
