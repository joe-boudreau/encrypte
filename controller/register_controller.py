from service.database_service import save_user, get_user
from service.utils import sha256_hash_hex, salt_generator
from user_passwords import UserData


def register_new_user(username, password, shared_secret):

    salt = salt_generator()
    password_hash = sha256_hash_hex(password, salt)

    new_up = UserData(username, password_hash, salt, shared_secret)

    save_user(new_up, password)


username = "joe"
password = "123456"
shared_secret = "ABC456"

register_new_user(username, password, shared_secret)

saved_user = get_user(username, password)

assert saved_user.username == username
assert saved_user.shared_secret == shared_secret

p_hash = sha256_hash_hex(password, saved_user.salt)
assert saved_user.password_hash == p_hash

