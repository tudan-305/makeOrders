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
        # 向左靠
        row1.addStretch()

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("出库方式：", fixedWidth=80))
        for num, i in enumerate(self.sale_modes, 1):
            btn = QRadioButton(i)
            btn.setFixedWidth(55)
            self.salemodes_group.addButton(btn, num)
            row2.addWidget(btn)
        row2.addStretch()

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("赠  品  单：", fixedWidth=80))
        for num, i in enumerate(self.order_modes, 1):
            btn = QRadioButton(i)
            btn.setFixedWidth(80)
            self.ordermodes_group.addButton(btn, num)
            row3.addWidget(btn)
        row3.addStretch()
        
        layout = QVBoxLayout(self)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
    
    @Slot(list)
    def set_salemode(self, hosp_info:list):
        """根据医院信息设定salemode区块的选项"""
        if hosp_info == []:
            # 没有选中医院时，清空salemode区块的选项
            group_list = [self.suppliers_group, self.salemodes_group, self.ordermodes_group]
            for group in group_list:
                group.setExclusive(False)
                for btn in group.buttons():
                    btn.setChecked(False)
                group.setExclusive(True)
            return
        
        supplier_id, sale_mode_id, order_mode_id = hosp_info
        supplier_btn = self.suppliers_group.button(supplier_id)
        if supplier_btn:
            supplier_btn.setChecked(True)
        else:
            print(f"don't match supplier_id:{supplier_id}")
        sale_mode_btn = self.salemodes_group.button(sale_mode_id)
        if sale_mode_btn:
            sale_mode_btn.setChecked(True)
        else:
            print(f"don't match sale_mode_id:{sale_mode_id}")
        order_mode_id = self.ordermodes_group.button(sale_mode_id)
        if order_mode_id:
            order_mode_id.setChecked(True)
        else:
            print(f"don't match order_mode_id:{order_mode_id}")