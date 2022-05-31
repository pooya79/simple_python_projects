from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal

class ClickableLabel(QLabel):
    # a custom label class to be clickable
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()