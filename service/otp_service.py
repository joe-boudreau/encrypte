import pyotp
import base64
import urllib.parse
import pyqrcode


def generate_QR_code(accountName, issuer, password):
    b = bytes(password, 'utf-8')
    encoded = base64.b32encode(b)
    val = encoded.decode("utf-8")
    URL = pyotp.totp.TOTP(val[:16]).provisioning_uri(accountName, issuer_name=issuer)
    qrcode = pyqrcode.create(URL)
    qrcode.svg('uca-url.svg', scale=1)
    qrcode.eps('uca-url.eps', scale=2)
    print(qrcode.terminal(quiet_zone=1))

def verify_otp_password(password, otp):
    b = bytes(password, 'utf-8')
    encoded = base64.b32encode(b)
    val = encoded.decode("utf-8")
    totp = pyotp.TOTP(val[:16])
    print("Current OTP:", totp.now())
    if otp == totp.now():
        print('Password valid')
    else:
        print('Password invalid')
