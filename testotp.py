import sys
from service.otp_service import *

accountname = input('Please enter your account name: ')

password = generate_QR_code(accountname, 'encrypté')

otp = input('Enter OTP')
verify_otp_password(password, otp)

