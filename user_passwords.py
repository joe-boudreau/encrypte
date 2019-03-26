
from service import utils

class UserData:

    def __init__(self, username, password_hash, salt, shared_secret, passwords=[]):
        self._username = username
        self._password_hash = password_hash
        self._salt = salt
        self._shared_secret = shared_secret
        self._passwords = passwords

    @property
    def username(self):
        return self._username

    @property
    def password_hash(self):
        return self._password_hash

    @property
    def salt(self):
        return self._salt

    @property
    def passwords(self):
        return self._passwords

    @property
    def shared_secret(self):
        return self._shared_secret

    @username.setter
    def username(self, val):
        if len(val) < 1:
            raise ValueError("Cannot set a blank username")
        self._username = val

    @password_hash.setter
    def password_hash(self, val):
        if len(val) < 1:
            raise ValueError("Cannot set a blank password")
        self._password_hash = val

    @salt.setter
    def salt(self, val):
        self._salt = val

    @passwords.setter
    def passwords(self, val):
        self._passwords = val

    @shared_secret.setter
    def shared_secret(self, val):
        self._shared_secret = val

    def add_password(self, password, service, create_date, expiry_date):
        newpassword = Password(password, service, create_date, expiry_date)
        self._passwords.append(newpassword)


class Password:

    def __init__(self, username, password, service, notes):
        self._username = username
        self._password = password
        self._service = service
        self._notes = notes
        self._id = utils.salt_generator()

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def service(self):
        return self._service

    @property
    def notes(self):
        return self._notes

    @property
    def id(self):
        return self._id

    @username.setter
    def username(self, val):
        self._username = val

    @password.setter
    def password(self, val):
        self._password = val

    @service.setter
    def service(self, val):
        self._service = val

    @notes.setter
    def notes(self, val):
        self._notes = val
