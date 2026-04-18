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
        
        for item in ['器械', '寄售', '折让', '赠送', '换货']:
            btn = QRadioButton(item)
            layout1.addWidget(btn)

        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel("产品单、赠品单："))
        for item in ['分开制作', '合并制作']:
            btn = QRadioButton(item)
            layout2.addWidget(btn)
        
        layout = QVBoxLayout(self)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
