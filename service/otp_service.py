import pyotp
import pyqrcode


def generate_QR_code(accountName, issuer):
    """
    Generates a QR code for the given account name and issuer. Returns the password and the QR code object as a tuple

    :param accountName: the account name (string)
    :param issuer: the issuer name (string)
    :returns: the generated password, a QR code object
    :rtype: tuple [String, QRCode]
    """
    password = pyotp.random_base32()
    URL = pyotp.totp.TOTP(password).provisioning_uri(accountName, issuer_name=issuer)
    qrcode = pyqrcode.create(URL)
    return password, qrcode


def verify_otp_password(password, otp):
    totp = pyotp.TOTP(password)
    print("Current OTP:", totp.now())
    if otp == totp.now():
        print('Password valid')
        return True
    else:
        print('Password invalid')
        return False
