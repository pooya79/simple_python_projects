import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QImageReader
from PyQt5.QtCore import QSize, QDir, Qt, QRect, QPoint
import cv2
import numpy as np

from utils import image_resize, edit_text
from main_window import Ui_MainWindow

IMAGE_FILE_FORMATS = tuple('.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats())

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # load ui
        self.setupUi(self)

        # connect side bar buttons
        self.trainButton.clicked.connect(self.train_button_clicked)
        self.testButton.clicked.connect(self.test_button_clicked)
        self.validButton.clicked.connect(self.valid_button_clicked)

        # connect add files and folders buttons
        self.addFileButton.clicked.connect(self.add_files_button_clicked)
        self.addFolderButton.clicked.connect(self.add_folder_button_clicked)
        self.selectPathButton.clicked.connect(self.add_folder_button_clicked)

        # connect save widgets
        self.pathIcon.clicked.connect(self.save_path_icon_clicked)
        self.pathLineEdit.textChanged.connect(self.save_path_edit_line_changed)
        self.differentPathCheck.stateChanged.connect(self.different_path_checkbox_checked)
        self.saveButton.clicked.connect(self.save_files)

        # connect transfer button
        self.transferButton.clicked.connect(self.transfer_button_clicked)

        # define data variables
        self.image_paths = {'train': [], 'test': [], 'valid': []}
        self.current_tab = 'train'
        self.save_paths = {'train': '', 'test': '', 'valid': ''}
        self.different_path_checkbox = {'test': False, 'valid': False}

        # hide assign different path in train tab
        self.differentPathCheck.setVisible(False)

        # implement a stack widget with three list widget in it
        self.stackWidget = QStackedWidget()
        self.gridLayout_2.addWidget(self.stackWidget)

        # create list widgets and add them to stack widget
        self.listWidgets = {}
        for tab in ['train', 'test', 'valid']:
            listWidget = QListWidget()
            self.stackWidget.addWidget(listWidget)
            # customize it
            listWidget.setStyleSheet('border: 0')
            listWidget.setViewMode(QListWidget.IconMode)
            listWidget.setResizeMode(QListWidget.Adjust)
            listWidget.setSpacing(20)
            listWidget.setIconSize(QSize(100, 100))
            listWidget.setUniformItemSizes(True)
            listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
            listWidget.itemDoubleClicked.connect(self.show_image_in_opencv)

            self.listWidgets[tab] = listWidget

        # hide stack widget when it is empty and show empty widget
        self.stackWidget.setVisible(False)
        self.emptyWidget.setVisible(True)

        self.show() 

    def train_button_clicked(self):
        # change style of side buttons
        self.adjust_side_buttons_style(self.trainButton, [self.testButton, self.validButton])

        # update current_tab variable
        self.current_tab = 'train'

        # hide assign different path and update its line edit path
        self.differentPathCheck.setVisible(False)
        self.pathLineEdit.setText(self.save_paths[self.current_tab])

        # enable path widgets
        self.pathIcon.setEnabled(True)
        self.pathLineEdit.setEnabled(True)

        # show empty widget if there is no image here else show images
        if self.image_paths[self.current_tab]:
            self.emptyWidget.setVisible(False)
            self.stackWidget.setVisible(True)
            self.stackWidget.setCurrentIndex(0)
        else:
            self.stackWidget.setVisible(False)
            self.emptyWidget.setVisible(True)

    def test_button_clicked(self):
        # change style of side buttons
        self.adjust_side_buttons_style(self.testButton, [self.trainButton, self.validButton])

        # update current_tab variable
        self.current_tab = 'test'

        # show assign different path checkbox and update its line edit path
        self.differentPathCheck.setVisible(True)
        self.differentPathCheck.setChecked(self.different_path_checkbox[self.current_tab])
        self.pathLineEdit.setText(self.save_paths[self.current_tab])

        # enable path widgets if its checkbox button is checked
        self.pathIcon.setEnabled(self.different_path_checkbox[self.current_tab])
        self.pathLineEdit.setEnabled(self.different_path_checkbox[self.current_tab])

        # show empty widget if there is no image here else show images
        if self.image_paths[self.current_tab]:
            self.emptyWidget.setVisible(False)
            self.stackWidget.setVisible(True)
            self.stackWidget.setCurrentIndex(1)
        else:
            self.stackWidget.setVisible(False)
            self.emptyWidget.setVisible(True)

    def valid_button_clicked(self):
        # change style of side buttons
        self.adjust_side_buttons_style(self.validButton, [self.testButton, self.trainButton])

        # update current_tab variable
        self.current_tab = 'valid'

        # show assign different path checkbox and update its line edit path
        self.differentPathCheck.setVisible(True)
        self.differentPathCheck.setChecked(self.different_path_checkbox[self.current_tab])
        self.pathLineEdit.setText(self.save_paths[self.current_tab])

        # enable path widgets if its checkbox is checked
        self.pathIcon.setEnabled(self.different_path_checkbox[self.current_tab])
        self.pathLineEdit.setEnabled(self.different_path_checkbox[self.current_tab])

        # show empty widget if there is no image here else show images
        if self.image_paths[self.current_tab]:
            self.emptyWidget.setVisible(False)
            self.stackWidget.setVisible(True)
            self.stackWidget.setCurrentIndex(2)
        else:
            self.stackWidget.setVisible(False)
            self.emptyWidget.setVisible(True)

    def add_files_button_clicked(self):
        # get files from file dialog
        formats = ['*.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        filters = "Image files (%s)" % ' '.join(formats)
        files_address = QFileDialog.getOpenFileNames(self, "Add Image Files", QDir.homePath(), filters)

        # if there is file
        if files_address[0]:
            # define a progress dialog
            progress_dialog = QProgressDialog("Getting Files ", "cancel", 0, len(files_address[0]), self)
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()
            progress_dialog.setValue(0)

            # append files to current tab list and show them
            self.image_paths[self.current_tab].extend(files_address[0])
            for i, image_path in enumerate(files_address[0]):
                progress_dialog.setValue(i)
                self.add_image_to_list_widget(image_path)
            progress_dialog.setValue(len(files_address[0]))

    def add_folder_button_clicked(self):
        # get folder path
        folder = QFileDialog.getExistingDirectory(self,
                                                    'Add Directory', QDir.homePath(),
                                                     QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        
        # get files in the folder
        if folder:
            files_list = os.listdir(folder)

            # define a progress dialog
            progress_dialog = QProgressDialog("Getting Files ", "cancel", 0, len(files_list), self)
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()

            # add image files in folder to our data and show them
            for i, file in enumerate(files_list):
                progress_dialog.setValue(i)
                # break process if it was canceled
                if progress_dialog.wasCanceled():
                    break
                # add only image files
                if file.endswith(IMAGE_FILE_FORMATS):
                    image_path = folder + "/" + file
                    self.image_paths[self.current_tab].append(image_path)
                    # add image to list widget
                    self.add_image_to_list_widget(image_path)

            progress_dialog.setValue(len(files_list))

    def add_image_to_list_widget(self, image_path):            
        # hide empty widget and show stacked widget
        self.emptyWidget.setVisible(False)
        self.stackWidget.setVisible(True)
        # add image to list widget
        item = QListWidgetItem(self.listWidgets[self.current_tab])
        item.setStatusTip(image_path)
        item.setText(edit_text.edit_text(os.path.basename(image_path)))
        pixmap = QPixmap(os.path.abspath(image_path))
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
        item.setIcon(QIcon(pixmap))

    def show_image_in_opencv(self, item):
        f = open(os.path.abspath(item.statusTip()), "rb")
        chunk = f.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        img = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
        img = image_resize.image_resize(img, 500)
        cv2.imshow(item.text(), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # print(self.listWiget.selectedItems())
        # print(self.listWiget.rect())
        # print(self.listWiget.indexAt(QPoint(0,self.listWiget.height())).row())

    def transfer_button_clicked(self):
        pass

    def save_path_icon_clicked(self):
        # get folder path
        folder = QFileDialog.getExistingDirectory(self,
                                                    'Select Saving Folder', QDir.homePath())

        # assign it to line edit and save path of current tab
        self.pathLineEdit.setText(folder)
        self.save_paths[self.current_tab] = folder

    def save_path_edit_line_changed(self, path):
        self.save_paths[self.current_tab] = path

    def different_path_checkbox_checked(self, check):
        self.different_path_checkbox[self.current_tab] = check
        
        # enable save path widgets
        self.pathIcon.setEnabled(check)
        self.pathLineEdit.setEnabled(check)

    def save_files(self):
        pass

    def adjust_side_buttons_style(self, clicked_button, not_clicked_buttons):
        # adjusting side buttons style after clicking them
        clicked_button.setStyleSheet("""
            QPushButton {
                background-color: #d9d9d9;
                color: #000;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
                color: #000;
            }
        """)
        for not_clicked_button in not_clicked_buttons:
            not_clicked_button.setStyleSheet("""
                QPushButton {
                    background-color: #000;
                    color: #fff;
                }
                QPushButton:hover {
                    background-color: #525252;
                }
            """)


if __name__ == "__main__":
    # start application when is running as main file
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
    