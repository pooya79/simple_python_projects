import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

from utils.qrangeslider import QRangeSlider
from utils.transfer_dialog_ui import Ui_Dialog


class TransferDialog(QDialog, Ui_Dialog):
    def __init__(self, number_of_files, *args, **kargs):
        super().__init__(*args, **kargs)
        self.number_of_files = number_of_files

        # setup ui
        self.setupUi(self)

        # connect buttons
        self.okPushButton.clicked.connect(self.ok_button_clicked)
        self.cancelPushButton.clicked.connect(self.cancel_button_clicked)

        # connect line edits
        self.trainNumberEdit.textChanged.connect(self.train_number_changed)
        self.trainPercentEdit.textChanged.connect(self.train_percent_changed)
        self.testNumberEdit.textChanged.connect(self.test_number_changed)
        self.testPercentEdit.textChanged.connect(self.test_percent_changed)
        self.validNumberEdit.textChanged.connect(self.valid_number_changed)
        self.validPercentEdit.textChanged.connect(self.valid_percent_changed)

        # make edit lines accept valid numbers
        self.trainPercentEdit.setValidator(QtGui.QIntValidator(0, 100))
        self.testPercentEdit.setValidator(QtGui.QIntValidator(0, 100))
        self.validPercentEdit.setValidator(QtGui.QIntValidator(0, 100))
        self.trainNumberEdit.setValidator(QtGui.QIntValidator(0, self.number_of_files))
        self.testNumberEdit.setValidator(QtGui.QIntValidator(0, self.number_of_files))
        self.validNumberEdit.setValidator(QtGui.QIntValidator(0, self.number_of_files))

        self.show()

    def train_number_changed(self, num):
        pass

    def train_percent_changed(self, percent):
        pass

    def test_number_changed(self, num):
        pass

    def test_percent_changed(self, percent):
        pass

    def valid_number_changed(self, num):
        pass

    def valid_percent_changed(self, percent):
        pass

    def ok_button_clicked(self):
        pass

    def cancel_button_clicked(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    transfer_dial = TransferDialog()
    app.exec()