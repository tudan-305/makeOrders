import json
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QHeaderView, QHBoxLayout, QMessageBox, 
    QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
)

class JsonTableEditor(QWidget):
    def __init__(self, json_path):
        super().__init__()
        self.json_path = json_path
        self.original_data = {}  # 缓存从文件读取的原始数据
        
        self.init_ui()
        self.load_json_to_table()
        
    def init_ui(self):
        self.setWindowTitle("JSON 字典编辑器")
        self.resize(600, 400)
        
        # 1. 创建表格
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["键 (Key)", "值 (Value)"])
        # 自适应列宽，最后一列拉伸
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 2. 创建按钮
        self.btn_add = QPushButton("新增行 (+)")
        self.btn_delete = QPushButton("删除选中行 (-)")
        self.btn_search = QPushButton("查找 / 筛选")
        self.btn_save = QPushButton("保存修改 (Save)")
        self.btn_cancel = QPushButton("取消修改 (Cancel)")
        
        # 按钮样式区分
        self.btn_save.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.btn_cancel.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        
        # 3. 绑定事件
        self.btn_add.clicked.connect(self.add_row)
        self.btn_delete.clicked.connect(self.delete_selected_row)
        self.btn_save.clicked.connect(self.save_to_json)
        self.btn_cancel.clicked.connect(self.cancel_changes)
        # 搜索功能为了轻量，这里直接用简单的滚动到目标或隐藏不匹配行
        self.btn_search.clicked.connect(self.search_key)
        
        # 4. 布局
        btn_layout_top = QHBoxLayout()
        btn_layout_top.addWidget(self.btn_add)
        btn_layout_top.addWidget(self.btn_delete)
        btn_layout_top.addWidget(self.btn_search)
        
        btn_layout_bottom = QHBoxLayout()
        btn_layout_bottom.addStretch()
        btn_layout_bottom.addWidget(self.btn_cancel)
        btn_layout_bottom.addWidget(self.btn_save)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(btn_layout_top)
        main_layout.addWidget(self.table)
        main_layout.addLayout(btn_layout_bottom)
        
        self.setLayout(main_layout)

    # --- 查（从 JSON 加载） ---
    def load_json_to_table(self):
        # 如果文件不存在，创建一个空的
        if not os.path.exists(self.json_path):
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
                
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.original_data = json.load(f)
        except json.JSONDecodeError:
            QMessageBox.warning(self, "错误", "JSON 文件格式损坏，已加载空字典。")
            self.original_data = {}
            
        self.fill_table(self.original_data)
        
    def fill_table(self, data_dict):
        self.table.setRowCount(0)  # 清空表格
        for key, value in data_dict.items():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(key)))
            self.table.setItem(row, 1, QTableWidgetItem(str(value)))

    # --- 增 ---
    def add_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        # 插入空白单元格供用户双击修改
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))
        # 自动滚动并选中新行
        self.table.scrollToBottom()
        self.table.setCurrentCell(row, 0)

    # --- 删 ---
    def delete_selected_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
        else:
            QMessageBox.information(self, "提示", "请先点击选择要删除的行！")

    # --- 查（查找过滤） ---
    def search_key(self):
        from PySide6.QtWidgets import QInputDialog
        search_text, ok = QInputDialog.getText(self, "查找", "输入要查找的键或值:")
        if not ok or not search_text:
            # 如果取消或输入为空，显示所有行
            for r in range(self.table.rowCount()):
                self.table.setRowHidden(r, False)
            return

        # 遍历筛选
        for r in range(self.table.rowCount()):
            key_item = self.table.item(r, 0)
            val_item = self.table.item(r, 1)
            
            key_match = search_text.lower() in key_item.text().lower() if key_item else False
            val_match = search_text.lower() in val_item.text().lower() if val_item else False
            
            # 不匹配的行隐藏
            self.table.setRowHidden(r, not (key_match or val_match))

    # --- 改 & 保存 ---
    def save_to_json(self):
        new_dict = {}
        # 遍历表格，组装成字典
        for r in range(self.table.rowCount()):
            key_item = self.table.item(r, 0)
            val_item = self.table.item(r, 1)
            
            key = key_item.text().strip() if key_item else ""
            val = val_item.text().strip() if val_item else ""
            
            if not key:
                QMessageBox.warning(self, "警告", f"第 {r+1} 行的键不能为空，保存中止！")
                return
            
            if key in new_dict:
                QMessageBox.warning(self, "警告", f"存在重复的键: '{key}'，保存中止！")
                return
                
            new_dict[key] = val
            
        # 写入文件并同步内存
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(new_dict, f, indent=4, ensure_ascii=False)
            
        self.original_data = new_dict
        QMessageBox.information(self, "成功", "数据已成功保存至 JSON 文件！")

    # --- 取消修改 ---
    def cancel_changes(self):
        reply = QMessageBox.question(
            self, "确认取消", "您确定要放弃所有未保存的修改吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # 重新用内存中的 original_data 覆盖表格
            self.fill_table(self.original_data)


if __name__ == "__main__":
    app = QApplication([])
    # 这里指定你的 json 文件路径
    json_filename = "settings.json"
    window = JsonTableEditor(json_filename)
    window.show()
    app.exec()