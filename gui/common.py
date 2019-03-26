import datetime
import sys

from PyQt5 import uic
from PyQt5.QtCore import QObject, QAbstractTableModel, QVariant, Qt
from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QTableView

from gui import images_rc #this is needed for image rendering
from service.utils import get_formatted_msg
from user_passwords import Password, UserData

def get_user(username, password):
    return UserData(username, password, "salt", "shared_secret", passwords)

class Common(QObject):

    def __init__(self,  username, password, parent=None):

        super(Common, self).__init__(parent)

        self.user = get_user(username, password)
        self.user_password = password

        self.window = uic.loadUi("gui/ui_files/common.ui")

        username_label = self.window.findChild(QLabel, 'username_label')
        username_label.setText(username_label.text().format(username))

        self.common_button = self.window.findChild(QPushButton, 'Add_button')
        self.common_button.clicked.connect(self.open_add_dialog)

        self.common_button = self.window.findChild(QPushButton, 'Remove_button')
        self.common_button.clicked.connect(self.remove_action)

        self.common_button = self.window.findChild(QPushButton, 'Quit_button')
        self.common_button.clicked.connect(self.quit_action)

        self.password_table = self.window.findChild(QTableView, 'Password_table')
        self.load_password_model()

        self.common_button = self.window.findChild(QTableView, 'Password_button')

    def show(self, msg=None, color="black"):
        if msg is not None:
            self.window.findChild(QLabel, 'result_msg').setText(get_formatted_msg(color, msg))
        self.window.show()

    def load_password_model(self):
        model = PasswordsModel(self.user.passwords)
        self.password_table.setModel(model)

    def open_add_dialog(self):
        return

    def remove_action(self, secret_id):
        return

    def quit_action(self):
        return

class PasswordsModel(QAbstractTableModel):
    def __init__(self, passwords, parent=None):
        """
        Args:
            passwords: a list of Password objects
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent)
        self.passwords = passwords
        if len(passwords) > 0:
            self.headerdata = list(vars(passwords[0]))
        else:
            self.headerdata = []

    def rowCount(self, parent):
        return len(self.passwords)

    def columnCount(self, parent):
        return len(self.headerdata)

    def get_password_attr(self, row_index, attr_index):
        return list(vars(self.passwords[row_index]).values())[attr_index]

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.get_password_attr(index.row(), index.column()))

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()
