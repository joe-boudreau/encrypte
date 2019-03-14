from PyQt5 import uic
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QPushButton, QMainWindow

from gui.register import Register
from gui import images_rc


class Login(QObject):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.window = uic.loadUi("ui_files/login.ui")

        register_button = self.window.findChild(QPushButton, 'register_button')
        register_button.clicked.connect(self.open_register)

        register_button = self.window.findChild(QPushButton, 'login_button')
        register_button.clicked.connect(self.attempt_login)

        self.register = Register()

    def open_register(self):
        self.register.show()
        self.window.destroy()

    def attempt_login(self):
        print("TODO")

    def show(self):
        self.window.show()
