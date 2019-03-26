from user_passwords import UserData, Password
from service.database_service import *



test_up = register_new_user("Test_User", "password", "1234")
saved_up = get_user("Test_User", "password")
user = add_password_to_user(saved_up, "password", "newpassword", "Facebook", "12/02/19", "12/03/19")
print(user.passwords[0].password)
