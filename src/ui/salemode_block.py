from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QLineEdit, QComboBox, 
                               QRadioButton)
from PySide6.QtCore import Signal, Slot

#区块2制作
class SalemodeBlock(QWidget):
    
    sale_mode = ['器械', '寄售', '折让', '赠送', '换货']
    sale_mode_btns = []
    layout = QVBoxLayout()
    layout1 = QHBoxLayout()
    layout2 = QHBoxLayout()

    for i in sale_mode:
        btn = QRadioButton(i)
        sale_mode_btns.append(btn)
        layout1.addWidget(btn)
    layout2.addWidget(QLabel("产品单、赠品单："))
    layout2.addWidget(QRadioButton("分开制作"))
    layout2.addWidget(QRadioButton("合并制作"))
    layout.addLayout(layout1)
    layout.addLayout(layout2)

    return layout
