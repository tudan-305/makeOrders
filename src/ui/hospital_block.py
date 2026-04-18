from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QDialog, QLineEdit, QComboBox, QDialogButtonBox,
    QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Signal, Slot
from src.models.dict_manager import hosp_mapping

class AddhospDialog(QDialog):
    final_report = Signal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self._was_modified = 0
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.setWindowTitle("医院管理")
        self.resize(500, 720)
        
        row1 = QHBoxLayout()
        self.nickname = QLineEdit(placeholderText="医院简称")
        self.nickname.setFixedWidth(80)
        self.holename = QLineEdit(placeholderText="医院全称")
        self.holename.setFixedWidth(240)
        self.clear_btn = QPushButton("清除")
        self.clear_btn.setFixedWidth(50)
        self.clear_btn.setEnabled(False)
        self.add_btn = QPushButton("添加医院")
        self.add_btn.setFixedWidth(80)
        self.add_btn.setEnabled(False)
        row1.addWidget(self.nickname)
        row1.addWidget(self.holename)
        row1.addWidget(self.clear_btn)
        row1.addWidget(self.add_btn)
        row2 = QHBoxLayout()
        self.show_status = QLabel("")
        row2.addWidget(self.show_status)

        row3 = QVBoxLayout()
        self.table = QTableWidget()
        self.set_table()
        row3.addWidget(self.table)

        layout = QVBoxLayout(self)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)

    def set_table(self):
        self.table.setRowCount(len(hosp_mapping.dict))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['医院简称', '医院全称'])
        self.table.horizontalHeader().setStretchLastSection(True)
        for row, (key, value) in enumerate(hosp_mapping.dict.items()):
            self.table.setItem(row, 0, QTableWidgetItem(key))
            self.table.setItem(row, 1, QTableWidgetItem(value))

    def connect_signals(self):
        self.nickname.textChanged.connect(self.check_inputs)
        self.holename.textChanged.connect(self.check_inputs)
        self.clear_btn.clicked.connect(self.on_clearbtn_clicked)
        self.add_btn.clicked.connect(self.on_addbtn_clicked)
        
    @Slot()
    def check_inputs(self):
        add_ready = bool(self.nickname.text().strip()) and bool(self.holename.text().strip())
        clear_ready = bool(self.nickname.text().strip()) or bool(self.holename.text().strip())
        self.add_btn.setEnabled(add_ready)
        self.clear_btn.setEnabled(clear_ready)

    @Slot()
    def on_clearbtn_clicked(self):
        self.nickname.clear()
        self.holename.clear()

    @Slot()
    def on_addbtn_clicked(self):
        dict_added = hosp_mapping.add(self.nickname.text(), self.holename.text())
        if dict_added:
            hosp_mapping.rank()
            hosp_mapping.save()
            self._was_modified += 1
            self.show_status.setStyleSheet("color:green")
            notice = "添加成功"
            self.set_table()
        else:
            self.show_status.setStyleSheet("color:red")
            notice = f"添加失败，{self.nickname.text()}已存在"
        self.show_status.setText(notice)

        

class HospitalBlock(QWidget):
    hosp_selected = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.refresh_hosp_combo()
        self.connect_signals()

    def setup_ui(self):
        #第一行：医院简称，清空按钮，添加医院
        row1 = QHBoxLayout()
        self.hosp_combo = QComboBox(placeholderText = "选择医院")
        self.hosp_combo.setFixedWidth(150)
        self.clear_btn = QPushButton("清除")
        self.clear_btn.setFixedWidth(50)
        self.add_hosp_btn = QPushButton("添加医院")
        row1.addWidget(self.hosp_combo)
        row1.addWidget(self.clear_btn)
        row1.addWidget(self.add_hosp_btn)
        #第二行：显示全称
        row2 = QHBoxLayout()
        self.show_holename_lbl = QLabel("全称:")
        self.show_holename_lbl.setFixedWidth(35)
        self.hosp_holename_lbl = QLabel("") 
        row2.addWidget(self.show_holename_lbl)
        row2.addWidget(self.hosp_holename_lbl)
        #一行二行加入布局
        layout = QVBoxLayout(self)
        layout.addLayout(row1)
        layout.addLayout(row2)
    
    def refresh_hosp_combo(self):
        self.hosp_combo.clear()
        for nickname, holename in hosp_mapping.dict.items():
            self.hosp_combo.addItem(nickname, holename)

    def connect_signals(self):
        self.clear_btn.clicked.connect(self.on_clear_btn_clicked)
        self.hosp_combo.currentIndexChanged.connect(self.on_index_changed)
        self.add_hosp_btn.clicked.connect(self.open_dialog)

    @Slot()
    def on_clear_btn_clicked(self):
        self.hosp_combo.setCurrentIndex(-1)

    @Slot()
    def on_index_changed(self, index):
        data = "" if index == -1 else self.hosp_combo.currentData()
        self.hosp_holename_lbl.setText(data)

    @Slot()
    def open_dialog(self):
        dialog = AddhospDialog()
        result = dialog.exec()
        if dialog._was_modified > 0:
            self.refresh_hosp_combo()