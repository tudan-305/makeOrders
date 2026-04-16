from PySide6.QtWidgets import QFrame

# 分割线制作
def create_line():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    return line