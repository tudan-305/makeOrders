import sys
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QLineEdit, QComboBox
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("无类直接使用布局示例")

btn = QPushButton(" 保存")
btn.setIcon(QIcon("/home/yingtc/Downloads/menu-burger.png"))
btn.setCheckable(True)

btn2 = QPushButton("X")
btn2.setFixedWidth(20)
edit = QLineEdit(placeholderText="enter something")



@Slot()
def on_btn_clicked():
    print("button clicked.")
@Slot()
def on_btn2_clicked():
    edit.clear()    

btn.clicked.connect(on_btn_clicked)
btn2.clicked.connect(on_btn2_clicked)

layout = QHBoxLayout()
layout.addWidget(edit)
layout.addWidget(btn)
layout.addWidget(btn2)

window.setLayout(layout)
window.show()
sys.exit(app.exec())
