import pyotp
import base64
import urllib.parse
import pyqrcode
import png

def generate_QR_code(accountName, issuer):
    password = pyotp.random_base32()
    URL = pyotp.totp.TOTP(password).provisioning_uri(accountName, issuer_name=issuer)
    qrcode = pyqrcode.create(URL)
    qrcode.png('Generated_QR_code.png', scale= 6) #Generate a png image of the qrcode
    qrcode.svg('uca-url.svg', scale=8) #generate html file containing the QRcode
    qrcode.eps('uca-url.eps', scale=4) #generate eps file
    print(qrcode.terminal(quiet_zone=1))
    return password
def verify_otp_password(password, otp):
    totp = pyotp.TOTP(password)
    print("Current OTP:", totp.now())
    if otp == totp.now():
        print('Password valid')
    else:
        print('Password invalid')
