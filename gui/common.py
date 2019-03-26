import sys

from PyQt5 import uic
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QLineEdit, QTableView

from gui.register import Register
from gui import images_rc #this is needed for image rendering
from service.database_service import get_user, authenticate
from service.utils import get_formatted_msg


class Common(QObject):

    def __init__(self,  username, password, parent=None):
        super(Common, self).__init__(parent)

        self.window = uic.loadUi("gui/ui_files/common.ui")

        self.common_button = self.window.findChild(QPushButton, 'Add_button')
        self.common_button.clicked.connect(self.Add_action)

        self.common_button = self.window.findChild(QPushButton, 'Remove_button')
        self.common_button.clicked.connect(self.Remove_action)

        self.common_button = self.window.findChild(QPushButton, 'Quit_button')
        self.common_button.clicked.connect(self.Quit_action)

        self.load_function(username, password)

        self.common_button = self.window.findChild(QTableView, 'Password_button')

    def show(self, msg=None, color="black"):
        if msg is not None:
            self.window.findChild(QLabel, 'result_msg').setText(get_formatted_msg(color, msg))
        self.window.show()

    def load_function(username, password):

        decode = get_user(username, password)
        info = decode.passwords

