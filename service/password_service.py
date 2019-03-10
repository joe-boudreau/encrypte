import json
from Crypto.Cipher import AES


def save_password_file(user_passwords_obj, filename):
    up_str = json.dumps(user_passwords_obj)

    aes = AES.new("this is a key", AES.MODE_CBC, "This is an IV")
    cipher_up_str = aes.encrypt(up_str)

    file = open(filename, 'w')
    file.write(cipher_up_str)
    file.close()


def read_password_file(filename):
    file = open(filename, 'r')
    cipher_up_str = file.read()
    file.close()

    aes = AES.new("this is a key", AES.MODE_CBC, "This is an IV")
    up_str = aes.decrypt(cipher_up_str)

    return json.loads(up_str)

