import random
import string

from Crypto.Hash import SHA256
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit


def sha256_hash_hex(data, salt=""):
    sha = SHA256.new()
    sha.update(data.encode("utf-8"))
    sha.update(salt.encode("utf-8"))
    return sha.hexdigest()


def sha256_hash_bytes(data, salt=""):
    sha = SHA256.new()
    sha.update(data.encode("utf-8"))
    sha.update(salt.encode("utf-8"))
    return sha.digest()


def salt_generator():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(10))


def get_formatted_msg(msg, color="black"):
    return "<html><head/><body><p align='center' style='color:{0}'><b>{1}</b><br/></p></body></html>".format(color, msg)


def maskUnmask(qObject, source, event):
    if event.type() == QtCore.QEvent.MouseButtonPress and source is qObject.password_input:
        qObject.password_input.setEchoMode(QLineEdit.Normal)
    elif event.type() == QtCore.QEvent.MouseButtonRelease and source is qObject.password_input:
        qObject.password_input.setEchoMode(QLineEdit.Password)
