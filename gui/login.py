import sys

from PyQt5 import uic
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QLineEdit

from gui.register import Register
from gui import images_rc #this is needed for image rendering
from service.database_service import get_user
from service.utils import get_formatted_msg


class Login(QObject):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.window = uic.loadUi("ui_files/login.ui")

        register_button = self.window.findChild(QPushButton, 'register_button')
        register_button.clicked.connect(self.open_register)

        register_button = self.window.findChild(QPushButton, 'login_button')
        register_button.clicked.connect(self.attempt_login)

        self.username_input = self.window.findChild(QLineEdit, 'username_input')
        self.password_input = self.window.findChild(QLineEdit, 'password_input')
        self.otp_input = self.window.findChild(QLineEdit, 'otp_input')

        self.register = Register(parent=self)

    def open_register(self):
        self.register.show()
        self.window.destroy()

    def attempt_login(self):
        username, password, otp_value = self.get_credentials()
        user = get_user(username, password)

        print("TODO")

    def show(self, msg=None):
        if msg is not None:
            self.window.findChild(QLabel, 'result_msg').setText(get_formatted_msg("green", msg))
        self.window.show()

    def get_credentials(self):
        return self.username_input.text(), self.password_input.text(), self.otp_shared_secret