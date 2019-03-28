import sys
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QObject, QAbstractTableModel, QVariant, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QTableView, QLineEdit, QMessageBox

from service import database_service
from gui import images_rc #this is needed for image rendering
from service.database_service import get_user
from service.utils import get_formatted_msg, maskUnmask
from user_passwords import Password, UserData

NONE = -1


class Common(QObject):

    def __init__(self,  username, password, parent=None):

        super(Common, self).__init__(parent)

        self.user = get_user(username, password)
        self.user_password = password

        self.window = uic.loadUi("gui/ui_files/common.ui")

        username_label = self.window.findChild(QLabel, 'username_label')
        username_label.setText(username_label.text().format(username))

        self.service_filter_input = self.window.findChild(QLineEdit, 'Filter_service')
        self.username_filter_input = self.window.findChild(QLineEdit, 'Filter_username')

        self.common_button = self.window.findChild(QPushButton, 'Add_button')
        self.common_button.clicked.connect(self.open_add_dialog)

        self.common_button = self.window.findChild(QPushButton, 'Edit_button')
        self.common_button.clicked.connect(self.open_edit_dialog)

        self.common_button = self.window.findChild(QPushButton, 'Remove_button')
        self.common_button.clicked.connect(self.remove_action)

        self.common_button = self.window.findChild(QPushButton, 'Quit_button')
        self.common_button.clicked.connect(self.quit_action)

        self.password_table = self.window.findChild(QTableView, 'Password_table')
        self.password_table.clicked.connect(self.unmask_password)
        self.load_password_model()


    def unmask_password(self, index):
        self.password_table.model().setData(index, None, Qt.DisplayRole)

    def show(self, msg=None, color="black"):
        if msg is not None:
            self.window.findChild(QLabel, 'result_msg').setText(get_formatted_msg(msg, color))
        self.window.show()

    def load_password_model(self):
        model = PasswordsModel(self.user.passwords)
        #get the user password and format them in an intelligible way for the tableviw
        self.password_table.setModel(model)

        service_filter_proxy_model = QSortFilterProxyModel()
        service_filter_proxy_model.setSourceModel(model)
        service_filter_proxy_model.setFilterKeyColumn(3)  # 4th column
        self.service_filter_input.textChanged.connect(service_filter_proxy_model.setFilterRegExp)
        self.password_table.setModel(service_filter_proxy_model)

        username_filter_proxy_model = QSortFilterProxyModel()
        username_filter_proxy_model.setSourceModel(service_filter_proxy_model)
        username_filter_proxy_model.setFilterKeyColumn(4)  # 5th column
        self.username_filter_input.textChanged.connect(username_filter_proxy_model.setFilterRegExp)
        self.password_table.setModel(username_filter_proxy_model)
        #set_model populates tableview with the user passwords

    def open_add_dialog(self):
        AddDialog(self).window.show()


    def open_edit_dialog(self):
        selected = self.password_table.selectionModel().selectedRows()

        if len(selected) != 1:
            self.show("You must select a password to remove", "red")
        else:
            Editdialog(self.user.passwords[selected[0].row()], self).window.show()

    def remove_action(self):
        selected = self.password_table.selectionModel().selectedRows()

        if len(selected) != 1:
            self.show("You must select a password to remove", "red")
        else:
            confirm = QMessageBox()
            confirm.setIcon(QMessageBox.Warning)
            confirm.setWindowTitle('Confirm')
            confirm.setText(get_formatted_msg('Are you sure you want to delete this password?', 'white'))
            confirm.setTextFormat(Qt.RichText)
            confirm.setStandardButtons(QMessageBox.Yes)
            confirm.addButton(QMessageBox.No)
            confirm.setDefaultButton(QMessageBox.No)
            confirm.setStyleSheet("background-color:black;color:white")
            if confirm.exec() == QMessageBox.Yes:
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
        self.password_index = 2
        self.headerdata = ['Username', 'Service', 'Password', 'Notes']
        self.selected = NONE

    def rowCount(self, parent):
        return len(self.passwords)

    def columnCount(self, parent):
        return len(self.headerdata)

    def get_password_attr(self, row_index, attr_index):
        attr_name = self.headerdata[attr_index]
        return vars(self.passwords[row_index])[attr_name]

    def data(self, index, role):
        if index.isValid():
            if index.column() == self.password_index:
                if (role == Qt.DisplayRole) & (index.row() == self.selected):
                    return QVariant(self.get_password_attr(index.row(), index.column()))
                elif role == Qt.DisplayRole:
                    return QVariant("************")
            elif role == Qt.DisplayRole:
                return QVariant(self.get_password_attr(index.row(), index.column()))
        return QVariant()

    def setData(self, index, value, role):
        if index.column() == self.password_index:
            self.selected = index.row()
        else:
            self.selected = NONE
        self.dataChanged.emit(index.sibling(0, 0), index.sibling(len(self.passwords)-1, len(self.headerdata)-1), [])
        return True

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()


class AddDialog(QObject):
    def __init__(self, parent=None):
        super(AddDialog, self).__init__(parent)
        self.window = uic.loadUi("gui/ui_files/add_or_edit_new_password.ui")

        self.common_button = self.window.findChild(QPushButton, 'save_button')
        self.common_button.clicked.connect(self.save_button)

        self.common_button = self.window.findChild(QPushButton, 'cancel_button')
        self.common_button.clicked.connect(self.cancel_action)

        self.username_input = self.window.findChild(QLineEdit, 'username_input')
        self.password_input = self.window.findChild(QLineEdit, 'password_input')
        self.password_input.installEventFilter(self)
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

    def eventFilter(self, source, event):
        maskUnmask(self, source, event)
        return super(AddDialog, self).eventFilter(source, event)

    def get_password(self):
        return self.username_input.text(), self.password_input.text(), self.service_name_input.text(), self.notes_input.text()

    def cancel_action(self):
        self.parent().show()
        self.window.hide()


class Editdialog(QObject):

    def __init__(self, password_to_modify, parent=None):
        super(Editdialog, self).__init__(parent)
        self.window = uic.loadUi("gui/ui_files/add_or_edit_new_password.ui")
        self.common_button = self.window.findChild(QPushButton, 'cancel_button')
        self.common_button.clicked.connect(self.cancel_action)

        self.username_input = self.window.findChild(QLineEdit, 'username_input')
        self.password_input = self.window.findChild(QLineEdit, 'password_input')
        self.password_input.installEventFilter(self)
        self.service_name_input = self.window.findChild(QLineEdit, 'service_name_input')
        self.notes_input = self.window.findChild(QLineEdit, 'notes_input')
        self.password_to_modify = password_to_modify
        self.edit_password()
        self.common_button = self.window.findChild(QPushButton, 'save_button')
        self.common_button.clicked.connect(self.update_info)

    def edit_password(self):

        self.username_input.setText(self.password_to_modify.username)
        self.password_input.setText(self.password_to_modify.password)
        self.service_name_input.setText(self.password_to_modify.service)
        self.notes_input.setText(self.password_to_modify.notes)

    def update_info(self):

        username, pwd, service, notes = self.get_password()
        if not pwd.strip() or not service.strip():
            self.window.findChild(QLabel, 'result_message').setText(get_formatted_msg("Please check that you at least entered the password and the services associated", "red"))
            return
        user = self.parent().user
        login_password = self.parent().user_password
        database_service.remove_password(self.parent().user, self.parent().user_password, self.password_to_modify)
        database_service.add_password_to_user(self.parent().user, login_password, username, pwd, service, notes)
        self.parent().load_password_model()
        self.parent().show("The new password information has been succesfuly added to the file")
        self.window.hide()

    def eventFilter(self, source, event):
        maskUnmask(self, source, event)
        return super(Editdialog, self).eventFilter(source, event)

    def get_password(self):
        return self.username_input.text(), self.password_input.text(), self.service_name_input.text(), self.notes_input.text()

    def cancel_action(self):
        self.parent().show()
        self.window.hide()
