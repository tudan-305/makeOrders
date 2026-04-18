from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QLineEdit, QComboBox, 
                               QRadioButton)
from PySide6.QtCore import Signal, Slot

#区块2制作
class SalemodeBlock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_ui()
    

    def set_ui(self):
        layout1 = QHBoxLayout()
        self.sale_mode = ['器械', '寄售', '折让', '赠送', '换货']
        self.sale_mode_btns = []
        

        for i in self.sale_mode:
            btn = QRadioButton(i)
            self.sale_mode_btns.append(btn)
            layout1.addWidget(btn)

        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel("产品单、赠品单："))
        layout2.addWidget(QRadioButton("分开制作"))
        layout2.addWidget(QRadioButton("合并制作"))
        
        layout = QVBoxLayout(self)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
