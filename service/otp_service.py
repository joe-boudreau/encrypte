import pyotp
import base64
import urllib.parse
import pyqrcode


#b = bytes('data encoded', 'utf-8')
#encoded = base64.b32encode(b)
#hotp = pyotp.HOTP(encoded) # secret key must be 32 based
#print(hotp.at(0))

#qrcode = "otpauth://totp/Secure%20App:alice%40google.com?secret=JBSWY3DPEHPK3PXP&issuer=Secure%20App"
accountNameEncoded ="alice@google.com"
issuerEncoded ="encrypte"
ekey = "JBSWY3DPEHPK3PXP"
hotp = "otpauth://hotp/%s?issuer=%s&secret=%s&counter=1" % (accountNameEncoded, issuerEncoded, ekey)
#query = urllib.parse.quote('otpauth://totp/Secure%20App:alice%40google.com?secret=JBSWY3DPEHPK3PXP&issuer=Secure%20App')
print(hotp)
URL = pyotp.totp.TOTP(ekey).provisioning_uri(accountNameEncoded, issuer_name=issuerEncoded)
qrcode = pyqrcode.create(URL, error='L', version=5, mode='binary')
qrcode.svg('uca-url.svg', scale=1)
qrcode.eps('uca-url.eps', scale=2)
print(qrcode.terminal(quiet_zone=1))