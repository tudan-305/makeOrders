import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView,
    QSpinBox, QMessageBox
)
from PySide6.QtCore import Qt

class ProductApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("产品管理 - 扫码添加")
        self.setGeometry(100, 100, 600, 400)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 顶部：扫码输入框 + 说明
        input_layout = QHBoxLayout()
        self.scan_input = QLineEdit()
        self.scan_input.setPlaceholderText("扫入商品二维码，或手动输入后添加")
        self.scan_input.returnPressed.connect(self.add_product_from_scan)
        input_layout.addWidget(self.scan_input)

        # 可选：手动添加按钮（备用）
        self.add_btn = QPushButton("手动添加")
        self.add_btn.clicked.connect(self.add_product_from_scan)
        input_layout.addWidget(self.add_btn)

        main_layout.addLayout(input_layout)

        # 产品表格：两列
        self.table = QTableWidget(0, 2)  # 0行，2列
        self.table.setHorizontalHeaderLabels(["产品名称", "数量"])
        # 让列宽自适应
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # 启用编辑（数量列使用自定义控件）
        # self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | 
        #                            QTableWidget.EditTrigger.EditKeyPressed)
        main_layout.addWidget(self.table)

        # 底部：删除选中行按钮
        self.delete_btn = QPushButton("删除选中产品")
        self.delete_btn.clicked.connect(self.delete_selected_product)
        main_layout.addWidget(self.delete_btn)

        # 存储产品名称与行号的映射，方便快速查找
        self.product_row_map = {}

    def add_product_from_scan(self):
        """从输入框获取产品名并添加（或增加数量）"""
        product_name = self.scan_input.text().strip()
        if not product_name:
            return

        # 检查产品是否已存在
        if product_name in self.product_row_map:
            row = self.product_row_map[product_name]
            # 获取当前数量控件的值并增加1
            spin_box = self.table.cellWidget(row, 1)
            if spin_box:
                new_qty = spin_box.value() + 1
                spin_box.setValue(new_qty)
        else:
            # 添加新行
            row = self.table.rowCount()
            self.table.insertRow(row)

            # 产品名称项（不可编辑）
            name_item = QTableWidgetItem(product_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)  # 禁止编辑名称
            self.table.setItem(row, 0, name_item)

            # 数量：使用 QSpinBox 作为单元格控件
            spin_box = QSpinBox()
            spin_box.setMinimum(1)
            spin_box.setMaximum(999999)
            spin_box.setValue(1)
            # 当数量改变时，可以在这里触发后续业务逻辑（如重新计算总价）
            spin_box.valueChanged.connect(lambda value, r=row: self.on_quantity_changed(r, value))
            self.table.setCellWidget(row, 1, spin_box)

            # 记录映射
            self.product_row_map[product_name] = row

            # 可选：滚动到新行
            self.table.scrollToBottom()
            

        # 清空输入框，准备下次扫码
        self.scan_input.clear()

    def on_quantity_changed(self, row, new_value):
        """数量被修改时的回调（可用于更新总价、日志等）"""
        product_name = self.table.item(row, 0).text()
        print(f"产品 '{product_name}' 数量变更为 {new_value}")

    def delete_selected_product(self):
        """删除当前选中的产品行"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "提示", "请先选中要删除的产品行")
            return

        product_name = self.table.item(current_row, 0).text()
        # 确认删除
        reply = QMessageBox.question(self, "确认删除", 
                                     f"确定要删除产品 '{product_name}' 吗？",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        # 移除映射
        del self.product_row_map[product_name]
        # 删除表格行
        self.table.removeRow(current_row)

        # 更新映射中后续行的索引（因为删除了中间一行，后面的行号会减1）
        self._refresh_row_map()

    def _refresh_row_map(self):
        """重建 product_row_map，保证行号与表格实际一致"""
        self.product_row_map.clear()
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 0)
            if name_item:
                product_name = name_item.text()
                self.product_row_map[product_name] = row

def main():
    app = QApplication(sys.argv)
    window = ProductApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()