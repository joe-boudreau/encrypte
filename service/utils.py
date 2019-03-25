import random
import string

from Crypto.Hash import SHA256


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
    return "<html><head/><body><p align='center' style='color:{}'><b>{}</b><br/></p></body></html>".format(color, msg)
