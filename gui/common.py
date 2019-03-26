import datetime
import sys

from PyQt5 import uic
from PyQt5.QtCore import QObject, QAbstractTableModel, QVariant, Qt
from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QTableView, QLineEdit
from service import database_service
from gui import images_rc #this is needed for image rendering
from service.database_service import get_user
from service.utils import get_formatted_msg
from user_passwords import Password

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
            self.window.findChild(QLabel, 'result_msg').setText(get_formatted_msg(msg, color))
        self.window.show()

    def load_password_model(self):
        model = PasswordsModel(self.user.passwords)
        #get the user password and format them in an intelligible way for the tableviw
        self.password_table.setModel(model)
        #set_model populates tableview with the user passwords

    def open_add_dialog(self):
        AddDialog(self).window.show()

    def remove_action(self):
        selected = self.password_table.selectionModel().selectedRows()

        if len(selected) != 1:
            self.show("You must select a password to remove", "red")
        else:
            self.delete_password(selected)

    def delete_password(self, selected):
        password_to_remove = self.user.passwords[selected[0].row()]
        database_service.remove_password(self.user, self.user_password, password_to_remove)
        self.load_password_model()
        self.show("The password for service: {} has been permanently deleted".format(password_to_remove.service))

    def quit_action(self):
        self.window.hide()
        sys.exit()
        return

    def show(self, msg=None, color="green"):
        if msg is not None:
            self.window.findChild(QLabel, 'result_msg').setText(get_formatted_msg(msg, color))
        self.window.show()

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

class AddDialog(QObject):
    def __init__(self, parent=None):
        super(AddDialog, self).__init__(parent)
        self.window = uic.loadUi("gui/ui_files/add_new_password.ui")

        self.common_button = self.window.findChild(QPushButton, 'save_button')
        self.common_button.clicked.connect(self.save_button)

        self.common_button = self.window.findChild(QPushButton, 'cancel_button')
        self.common_button.clicked.connect(self.cancel_action)

        self.username_input = self.window.findChild(QLineEdit, 'username_input')
        self.password_input = self.window.findChild(QLineEdit, 'password_input')
        self.service_name_input = self.window.findChild(QLineEdit, 'service_name_input')
        self.notes_input = self.window.findChild(QLineEdit, 'notes_input')

    def save_button(self):

        username, pwd, service, notes = self.get_password()
        if not pwd.strip() or not service.strip():
            self.window.findChild(QLabel, 'result_message').setText(get_formatted_msg("Please check that you at least entered the password and the services associated", "red"))
            return
        user = self.parent().user
        login_password = self.parent().user_password
        database_service.add_password_to_user(user, login_password, username, pwd, service, notes)

        self.parent().load_password_model()
        self.parent().show("The new password information has been succesfuly added to the file")
        self.window.hide()

    def get_password(self):

        return self.username_input.text(), self.password_input.text(), self.service_name_input.text(), self.notes_input.text()

    def cancel_action(self):
        self.parent().show()
        self.window.hide()


# password1 = Password("gmail","secret1", "Facebook")
# password2 = Password("like","secret2", "Google")
# password3 = Password("brand","secret1", "Pornhub")
#
# passwords = [password1, password2, password3]
#
# app = QApplication(sys.argv)
# common = Common("test", "password")
# common.show()
# sys.exit(app.exec_())