import sys
from rich import print
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout
app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout(window)
table = QTableWidget(10, 3)
print(dir(table))
print(table.horizontalHeader())
layout.addWidget(table)
window.show()
sys.exit(app.exec())
