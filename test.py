from user_passwords import UserData, Password
from service.database_service import *

password1 = Password("pword1", "Facebook", "2019-06-03", "2020-01-01")
password2 = Password("pword2", "Gmail", "2019-22-01", "2020-12-31")

test_up = UserData("Test User", "password hash abc123", [password1, password2])

save_user(test_up)

saved_up = get_user("test_file.encrypted")

print(saved_up.passwords[1].password)
