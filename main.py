from PIL import Image, UnidentifiedImageError
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from ui.main_window_ui import Ui_MainWindow
import re
import sys


class PyGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        self.filenames = []
        super(PyGUI, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.handle_browse_button)
        self.ui.pushButton_2.clicked.connect(self.handle_convert_button)

    def handle_browse_button(self):
        if self.ui.pushButton.text() == "Clear Selection":
            self.filenames.clear()
            self.ui.pushButton.setText("Select Source Files")
            self.handle_ui_checkboxes()
        else:
            if self.ui.radioButton.isChecked():
                self.filenames.clear()
                dlg = QtWidgets.QFileDialog()
                dlg.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
                dlg.setNameFilters(["Images (*.jpg)"])
                dlg.selectNameFilter("Images (*.jpg)")
                if dlg.exec_():
                    self.filenames.append(dlg.selectedFiles())
                    self.handle_ui_checkboxes()
            elif self.ui.radioButton_2.isChecked():
                self.filenames.clear()
                dlg = QtWidgets.QFileDialog()
                dlg.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
                dlg.setNameFilters(["Images (*.png)"])
                dlg.selectNameFilter("Images (*.png)")
                if dlg.exec_():
                    self.filenames.append(dlg.selectedFiles())
                    self.handle_ui_checkboxes()
            elif self.ui.radioButton_3.isChecked():
                self.filenames.clear()
                dlg = QtWidgets.QFileDialog()
                dlg.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
                dlg.setNameFilters(["Images (*.png *.jpg)"])
                dlg.selectNameFilter("Images (*.png *.jpg)")
                if dlg.exec_():
                    self.filenames.append(dlg.selectedFiles())
                    self.handle_ui_checkboxes()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(2)
                msg.setText("Processing mode has to be selected before input files!")
                msg.setWindowTitle("Missing processing")
                msg.exec_()

    def handle_convert_button(self):
        if (
            self.ui.radioButton.isChecked()
            or self.ui.radioButton_2.isChecked()
            or self.ui.radioButton_3.isChecked()
        ):
            if self.filenames == []:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(2)
                msg.setText("No input files were selected for processing")
                msg.setWindowTitle("Missing input")
                msg.exec_()
            else:
                self.image_conversion()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(2)
            msg.setText("First select processing mode and input files")
            msg.setWindowTitle("Missing processing")
            msg.exec_()

    def handle_ui_checkboxes(self):
        if self.filenames == []:
            self.ui.pushButton.setText("Select Source Files")
            self.ui.radioButton.setEnabled(True)
            self.ui.radioButton_2.setEnabled(True)
            self.ui.radioButton_3.setEnabled(True)
        else:
            self.ui.pushButton.setText("Clear Selection")
            self.ui.radioButton.setEnabled(False)
            self.ui.radioButton_2.setEnabled(False)
            self.ui.radioButton_3.setEnabled(False)

    def handle_finish(self):
        self.filenames.clear()
        self.handle_ui_checkboxes()

    def os_check_for_path(self):
        if sys.platform == "win32":
            return "\\"
        else:
            return "/"

    def success_message_box(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(1)
        msg.setText("Image(s) processed succesfully!")
        msg.setWindowTitle("Success!")
        msg.exec_()

    def image_conversion(self):
        try:
            dlg = QtWidgets.QFileDialog()
            dlg.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
            if self.ui.radioButton.isChecked():
                dlg.setNameFilters(["Images (*.png)"])
                dlg.selectNameFilter("Images (*.png)")
                path = []
                if dlg.exec_():
                    path = dlg.selectedFiles()
                if path != []:
                    for file in self.filenames[0]:
                        image = Image.open(file)
                        imagepath = (
                            path[0]
                            + re.search(r"[\/|\\]([^/\\]+)[\..+]", file).group()
                            + "png"
                        )
                        image.save(imagepath)
                    self.success_message_box()
                    self.handle_finish()
            if self.ui.radioButton_2.isChecked():
                dlg.setNameFilters(["Images (*.png)"])
                dlg.selectNameFilter("Images (*.png)")
                path = []
                if dlg.exec_():
                    path = dlg.selectedFiles()
                if path != []:
                    for file in self.filenames[0]:
                        image = Image.open(file)
                        imagepath = (
                            path[0]
                            + re.search(r"[\/|\\]([^/\\]+)[\..+]", file).group()
                            + "jpg"
                        )
                        image.save(imagepath)
                    self.success_message_box()
                    self.handle_finish()
            elif self.ui.radioButton_3.isChecked():
                dlg.setNameFilters(["Images (*.gif)"])
                dlg.selectNameFilter("Images (*.gif)")
                path = []
                if dlg.exec_():
                    path = dlg.selectedFiles()
                images = []
                imgsize = ()
                counter = 0
                for file in self.filenames[0]:
                    images.append(Image.open(file))
                    if imgsize == ():
                        imgsize = images[counter].size
                    else:
                        images[counter] = images[counter].resize(imgsize)
                    counter += 1
                imagepath = path[0] + self.os_check_for_path() + "result.gif"
                if path != []:
                    images[0].save(
                        imagepath,
                        format="GIF",
                        save_all=True,
                        append_images=images[1:],
                        optimize=False,
                        duration=self.ui.spinBox.value(),
                        loop=not self.ui.checkBox.isChecked(),
                    )
                    self.success_message_box()
                    self.handle_finish()
        except UnidentifiedImageError as err:
            message = str(err).split("'")[1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(3)
            msg.setText("The following image could not be processed:")
            msg.setInformativeText(message)
            msg.setWindowTitle("Unidentified image")
            msg.exec_()


def main():
    app = QApplication(sys.argv)
    form = PyGUI()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
