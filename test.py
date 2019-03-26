from user_passwords import UserData, Password
from service.database_service import *

username = "Test"
password = "Secure"



save_user(test_up)

saved_up = get_user("test_file.encrypted")

print(saved_up.passwords[1].password)
