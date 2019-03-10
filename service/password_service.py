import json
import jsonpickle
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def save_password_file(user_passwords_obj, filename):
    #up_str = json.dumps(user_passwords_obj)

    up_str = jsonpickle.encode(user_passwords_obj)

    up_str = pad(up_str)
    aes = AES.new("this is a key444", AES.MODE_CBC, "This is an IV444")
    cipher_up_str = aes.encrypt(up_str)

    file = open(filename, 'wb')
    file.write(cipher_up_str)
    file.close()


def read_password_file(filename):
    file = open(filename, 'rb')
    cipher_up_str = file.read()
    file.close()

    aes = AES.new("this is a key444", AES.MODE_CBC, "This is an IV444")
    up_str = aes.decrypt(cipher_up_str)

    #return json.loads(up_str)
    print(up_str)
    decode = jsonpickle.decode(unpad(up_str))
    return decode

