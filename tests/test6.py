import sys
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QWidget
from PySide6.QtCore import Qt
app = QApplication(sys.argv)
window = QWidget()
table = QTableWidget(2, 2)
item = QTableWidgetItem("ggood")
table.setItem(0, 0, item)
print(bin(item.flags().value))
print(bin((~Qt.ItemIsEditable).value))
table.show()

sys.exit(app.exec())