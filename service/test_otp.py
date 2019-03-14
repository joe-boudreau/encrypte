import sys
from service.otp_service import *

accountname = input('Please enter your account name: ')
password = input('Please enter your password : ')
if (len(password)<10):

    sys.exit("Error ! the password need to be at least 10 character long")
else:
    generate_QR_code(accountname, 'encrypte', password)

    otp = input('Enter OTP')
    verify_otp_password(password, otp)
