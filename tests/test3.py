import sys
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import Slot



class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mapping = {
            "张三": "admin",
            "李四": "user",
            "王五": "guest",
        }
        self.set_ui()
        self.connect_signals()
        
    def set_ui(self):
        layout = QVBoxLayout(self)

        self.combo = QComboBox()
        for text, data in self.mapping.items():
            self.combo.addItem(text, data)
        self.label = QLabel("")

        layout.addWidget(self.combo)
        layout.addWidget(self.label)

    def connect_signals(self):
        self.combo.currentTextChanged.connect(self.on_text_changed)
    
    @Slot()
    def on_text_changed(self, text):
        self.label.setText(str(self.combo.currentData()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_window = Window()
    my_window.show()
    sys.exit(app.exec())