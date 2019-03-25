import sys

from PyQt5 import uic
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QLineEdit

from gui.register import Register
from gui import images_rc #this is needed for image rendering
from service.database_service import get_user, authenticate
from service.utils import get_formatted_msg


class Common(QObject):

    def __init__(self, parent=None):
        super(Common, self).__init__(parent)

        self.window = uic.loadUi("ui_files/common.ui")

    def show(self, msg=None, color="black"):
        if msg is not None:
            self.window.findChild(QLabel, 'result_msg').setText(get_formatted_msg(color, msg))
        self.window.show()
