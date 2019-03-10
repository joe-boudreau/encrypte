from user_passwords import UserPasswords, Password
from service.password_service import *

password1 = Password("pword1", "Facebook", "2019-06-03", "2020-01-01")
password2 = Password("pword2", "Gmail", "2019-22-01", "2020-12-31")

test_up = UserPasswords("Test User", "password hash abc123", [password1, password2])


save_password_file(test_up, "test_file.encrypted")

saved_up = read_password_file("test_file.encrypted")

print(saved_up.passwords[1].password)
