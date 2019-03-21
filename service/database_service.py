import json
import jsonpickle
from Crypto.Cipher import AES

from service.utils import sha256_hash_hex, sha256_hash_bytes, salt_generator
from user_passwords import UserData

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]


def register_new_user(username, password, shared_secret):

    salt = salt_generator()
    password_hash = sha256_hash_hex(password, salt)

    new_up = UserData(username, password_hash, salt, shared_secret)

    save_user(new_up, password)


def save_user(user, password):

    up_str = jsonpickle.encode(user)
    up_str = pad(up_str)

    key = sha256_hash_bytes(password)
    aes = AES.new(key, AES.MODE_CBC, "Static 16 Bytes!") #TODO: Make IV dynamic?
    cipher_up_str = aes.encrypt(up_str)

    filename = get_user_filename(user.username)
    file = open(filename, 'wb')
    file.write(cipher_up_str)
    file.close()


def get_user(username, password):
    """
    Retrieves the saved user data, if it exists and can be decrypted successfully. If it does not, an Error is raised.

    :param username: the account name (string)
    :param password: the issuer name (string)
    :returns: the generated password, a QR code object
    :rtype: tuple [String, QRCode]
    """
    filename = get_user_filename(username)

    file = open(filename, 'rb')
    cipher_up_str = file.read()
    file.close()

    key = sha256_hash_bytes(password)
    aes = AES.new(key, AES.MODE_CBC, "Static 16 Bytes!") #TODO: Make IV dynamic?
    up_str = aes.decrypt(cipher_up_str)

    decode = jsonpickle.decode(unpad(up_str))
    return decode


def get_user_filename(username):
    return "user_" + sha256_hash_hex(username) + ".encrypted"

