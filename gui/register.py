from gui import images_rc  # this is needed for image rendering

from PyQt5 import uic
from PyQt5.QtCore import QObject, QByteArray
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QCommandLinkButton

from service import otp_service
from service.database_service import register_new_user
from service.otp_service import verify_otp_password
from service.utils import get_formatted_msg


class Register(QObject):

    def __init__(self, parent=None):
        super(Register, self).__init__(parent)
        self.window = uic.loadUi("ui_files/register.ui")

        self.continue_button = self.window.findChild(QPushButton, 'continue_button')
        self.continue_button.clicked.connect(self.continue_action)


        self.cancel_button = self.window.findChild(QPushButton, 'cancel_button')
        self.cancel_button.clicked.connect(self.cancel_action)

        self.username_input = self.window.findChild(QLineEdit, 'username_input')
        self.password_input = self.window.findChild(QLineEdit, 'password_input')

        # TODO: Use username entered instead of hardcoded
        self.otp_shared_secret, qr_code = otp_service.generate_QR_code("encrypte user", "encrypte")

        b64array = QByteArray.fromBase64(qr_code.png_as_base64_str(scale=6).encode('ascii'))
        qr_code_image = QImage()
        qr_code_image.loadFromData(b64array, "PNG")

        self.qr_code_label = self.window.findChild(QLabel, 'qr_code_image')
        self.qr_code_label.setPixmap(QPixmap.fromImage(qr_code_image))

        self.confirm_dialog = RegisterConfirm(self)

    def continue_action(self):
        self.confirm_dialog.show()

    def cancel_action(self):
        self.parent().show()
        self.window.destroy()

    def show(self):
        self.window.show()

    def get_credentials(self):
        return self.username_input.text(), self.password_input.text(), self.otp_shared_secret


class RegisterConfirm(QObject):

    def __init__(self, parent=None):
        super(RegisterConfirm, self).__init__(parent)
        self.window = uic.loadUi("ui_files/register_confirm.ui")

        self.username_input = self.window.findChild(QLineEdit, 'username_input')
        self.password_input = self.window.findChild(QLineEdit, 'password_input')
        self.otp_input = self.window.findChild(QLineEdit, 'otp_input')

        self.result_message = self.window.findChild(QLabel, 'result_message')
        self.result_message.setText("")

        self.register_button = self.window.findChild(QCommandLinkButton, 'register_button')
        self.register_button.clicked.connect(self.register_action)

        self.cancel_button = self.window.findChild(QPushButton, 'cancel_button')
        self.cancel_button.clicked.connect(self.cancel_action)

    def register_action(self):
        username, password, otp_shared_secret = self.parent().get_credentials()

        username_confirm = self.username_input.text()
        password_confirm = self.password_input.text()
        otp_value = self.otp_input.text()

        registration_successful = (username == username_confirm) & \
                                  (password == password_confirm) & \
                                  verify_otp_password(otp_shared_secret, otp_value)

        if registration_successful:
            register_new_user(username, password, otp_shared_secret)
            self.parent().parent().show("Registration Successful!") #open login window
            self.parent().window.destroy() #close register window
            self.window.destroy() #close dialog
        else:
            self.result_message.setText(get_formatted_msg("red", "Incorrect Credentials! Try again"))

    def cancel_action(self):
        self.parent().show()
        self.window.destroy()

    def show(self):
        self.window.show()

