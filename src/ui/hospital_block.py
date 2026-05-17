from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QDialog, QLineEdit, QComboBox, QDialogButtonBox,
    QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Signal, Slot, Qt, QTimer
from src.models.dict_manager import hosp_mapping

class AddhospDialog(QDialog):
    final_report = Signal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self._was_modified = 0
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """添加医院窗口"""
        self.setWindowTitle("医院管理")
        self.resize(500, 720)
        # 第一行
        # 医院简称、全称
        row1 = QHBoxLayout()
        self.nickname = QLineEdit(placeholderText="医院简称")
        self.nickname.setFixedWidth(80)
        self.holename = QLineEdit(placeholderText="医院全称")
        self.holename.setFixedWidth(240)
        # 预设销售模式
        self.sm1_combo = QComboBox()
        self.sm1_combo.setFixedWidth(35)
        self.sm1_combo.addItems([str(i) for i in [1, 2]])
        self.sm2_combo = QComboBox()
        self.sm2_combo.setFixedWidth(35)
        self.sm2_combo.addItems([str(i) for i in [1,2,3,4,5]])
        self.sm3_combo = QComboBox()
        self.sm3_combo.setFixedWidth(35)
        self.sm3_combo.addItems([str(i) for i in [1,2]])
        # 输入错误快速清除按钮,输入框无内容不可用
        self.clear_btn = QPushButton("清除")
        self.clear_btn.setFixedWidth(50)
        
        self.clear_btn.setEnabled(False)
        # 加入row1
        row1.addWidget(self.nickname)
        row1.addWidget(self.holename)
        row1.addWidget(self.sm1_combo)
        row1.addWidget(self.sm2_combo)
        row1.addWidget(self.sm3_combo)
        row1.addWidget(self.clear_btn)
        
        
        # 第三行 添加按钮，删除按钮，显示添加成功失败的状态
        row2 = QHBoxLayout()
        self.add_btn = QPushButton("添加医院")
        self.add_btn.setFixedWidth(80)
        self.add_btn.setEnabled(False)
        self.del_btn = QPushButton("删除选中")
        self.del_btn.setFixedWidth(80)
        self.del_btn.setStyleSheet("background-color:#B22222;color:white;")
        self.del_btn.setEnabled(False)
        self.show_status = QLabel("\t\t\t")

        row2.addWidget(self.add_btn)
        row2.addWidget(self.del_btn)

        row2.addWidget(self.show_status)
        # 第三行 显示医院表格
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
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['医院简称', '医院全称', '默认出库方式'])
        # self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        for i in range(1, self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        for row, (key, (value, mode)) in enumerate(hosp_mapping.dict.items()):
            self.table.setItem(row, 0, QTableWidgetItem(key))
            self.table.setItem(row, 1, QTableWidgetItem(value))
            # layout = QHBoxLayout()
            # button = QPushButton("del")
            # button.setFixedHeight(15)
            # button.setFixedWidth(40)

            # button.setStyleSheet("background-color:red;color:white")
            # layout.addWidget(button)
            # layout.addWidget(QLabel(str(mode)))
            # container = QWidget()
            # container.setLayout(layout)
            # self.table.setCellWidget(row, 2, container)
            
            self.table.setItem(row, 2, QTableWidgetItem(str(mode)))
            

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
        self.clear_btn.setStyleSheet("background-color:#B22222;color:white;" if clear_ready else "")

    @Slot()
    def on_clearbtn_clicked(self):
        self.nickname.clear()
        self.holename.clear()

    @Slot()
    def on_addbtn_clicked(self):
        """添加医院，标识字典改动的状态码+1，最后窗口结束时，只要状态码>0,就需要更新主界面中的qcombo，
        并且展示提示：成功显示绿色提示，失败红色提示"""
        dict_added = hosp_mapping.add(self.nickname.text(), self.holename.text())
        if dict_added:
            self._was_modified += 1
            statu_color = "green"
            notice = "添加成功"
            self.set_table()
        else:
            statu_color = "red"
            notice = f"添加失败，{self.nickname.text()}已存在"
        self.show_status.setText(notice)
        self.show_status.setStyleSheet(f"color:{statu_color}")

        

class HospitalBlock(QWidget):
    # 医院选中时，发射列表，用来设定salemode里面的供应商和出库方式等选项
    hosp_selected = Signal(list)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.refresh_hosp_combo()
        self.connect_signals()

    def setup_ui(self):
        #第一行：医院简称，清空按钮，添加按钮
        row1 = QHBoxLayout()
        self.hosp_combo = QComboBox(placeholderText = "选择医院")
        self.clear_btn = QPushButton("清除")
        self.clear_btn.setFixedWidth(50)
        self.add_hosp_btn = QPushButton("添加医院")
        self.add_hosp_btn.setFixedWidth(100)
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
        """清空，然后重新添加dict里面的每项到qcombo，得到刷新效果"""
        self.hosp_combo.clear()
        for nickname, value in hosp_mapping.dict.items():
            self.hosp_combo.addItem(nickname, value)

    def connect_signals(self):
        self.clear_btn.clicked.connect(self.on_clear_btn_clicked)
        self.hosp_combo.currentIndexChanged.connect(self.on_index_changed)
        self.add_hosp_btn.clicked.connect(self.open_dialog)

    @Slot()
    def on_clear_btn_clicked(self):
        self.hosp_combo.setCurrentIndex(-1)

    @Slot()
    def on_index_changed(self, index):
        if index == -1:
            data = ""
            data_signal = []
            
        else:
            data = self.hosp_combo.currentData()[0]
            data_signal = self.hosp_combo.currentData()[1]
        self.hosp_holename_lbl.setText(data)
        self.hosp_selected.emit(data_signal)

    @Slot()
    def open_dialog(self):
        dialog = AddhospDialog()
        dialog.exec()
        if dialog._was_modified > 0:
            self.refresh_hosp_combo()