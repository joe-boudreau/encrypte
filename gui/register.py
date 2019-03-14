from PyQt5 import uic
from PyQt5.QtCore import QObject
from gui import images_rc


class Register(QObject):

    def __init__(self, parent=None):
        super(Register, self).__init__(parent)

        self.window = uic.loadUi("ui_files/register.ui")

    def show(self):
        self.window.show()
