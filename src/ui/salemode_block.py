from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,QPushButton,
                               QButtonGroup, QLabel, QLineEdit, QRadioButton)
from PySide6.QtCore import Signal, Slot

#区块2制作
class SalemodeBlock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.suppliers = {"喜鱼":"杭州喜鱼医疗科技有限公司",
                          "九州通": "浙江九州通医疗器械有限公司"}
        self.sale_modes = ['器械', '寄售', '折让', '赠送', '换货']
        self.order_modes = ['分开制作', '合并制作']
        # 创建三个隔离的qbuttongroup 来管理qradiobutton
        self.suppliers_group = QButtonGroup()
        self.salemodes_group = QButtonGroup()
        self.ordermodes_group = QButtonGroup()
        self.set_ui()

    def set_ui(self):
        # 创建QRadioButton放入QButtonGroup并放入layout
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("供  应  商：", fixedWidth=80))
        for num, i in enumerate(self.suppliers.keys(), 1):
            btn = QRadioButton(i)
            btn.setFixedWidth(80)
            self.suppliers_group.addButton(btn, num)
            row1.addWidget(btn)
        row1.addStretch()

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("出库方式：", fixedWidth=80))
        for i in self.sale_modes:
            btn = QRadioButton(i)
            btn.setFixedWidth(55)
            self.salemodes_group.addButton(btn)
            row2.addWidget(btn)
        row2.addStretch()

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("赠  品  单：", fixedWidth=80))
        for i in self.order_modes:
            btn = QRadioButton(i)
            btn.setFixedWidth(80)
            self.ordermodes_group.addButton(btn)
            row3.addWidget(btn)
        row3.addStretch()
        
        layout = QVBoxLayout(self)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)