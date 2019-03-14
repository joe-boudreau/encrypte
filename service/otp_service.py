import pyotp
import base64
import urllib.parse
import pyqrcode


def generate_QR_code(accountName, issuer):
    password = pyotp.random_base32()
    URL = pyotp.totp.TOTP(password).provisioning_uri(accountName, issuer_name=issuer)
    qrcode = pyqrcode.create(URL)
    qrcode.svg('uca-url.svg', scale=1)
    qrcode.eps('uca-url.eps', scale=2)
    print(qrcode.terminal(quiet_zone=1))
    return password
def verify_otp_password(password, otp):
    totp = pyotp.TOTP(password)
    print("Current OTP:", totp.now())
    if otp == totp.now():
        print('Password valid')
    else:
        print('Password invalid')
