import sys

from PyQt5.QtWidgets import QApplication
from gui.login import Login

app = QApplication(sys.argv)
login = Login()
login.show()
sys.exit(app.exec_())

