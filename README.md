# encrypte
### Password Vault with TOTP based 2FA

This application is used to store and protect user's password in a local machine. Unlike the other solutions available online , that store user passwords in the cloud, our solution warranties that the user information will not be collected or used by a third-party.​

Our application is extremely secure. It uses a 2 FA (Factor Authentication) : the user password and a OTP (One-Time-Password) that is generated by the user's phone and changes every 30 seconds.​

The user password is not stored by the application. Indeed, the password is hashed using the SHA-256 cryptographic function which is the most secure hash function currently available in the market. We also use a salt for the password before hashing it, so that, the application never generates the same hash even for user using the same password.​

The password file populated by the user is encrypted using  AES (Advanced Encryption Standard).  This encryption standard is used by the NSA for top-secret information encryption and is the most secure encryption standard currently available on the market [3]. We used the user password hash which is 256 bits long as a key for the AES encryption.​The hash is also use as file name so that it's not possible for an attacker to figure out the username.

When the user is logged in the passwords stay hidden and only reveals upon user’s request (figure 3). Therefore, encrypté maintain the user privacy even when is logged in. that is a significatve improvement compared to the password vault solutions available online.
