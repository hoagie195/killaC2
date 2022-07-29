import base64
import binascii
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

class dataEncryptor:

    def __init__(self) -> None:
        pass

    def encrypting(self,data,key):
        enc = bytes(key, "utf-8")
        data = data.encode("utf-8")
        iv = b'\x9a\x95\xb9\xe9#c\xd9\xa5\x92CG\xf9)\x0e\xf5x'
        cipher = AES.new(enc, AES.MODE_CBC, iv)
        return str(base64.b64encode(cipher.encrypt(pad(data,16))),'utf-8')

    def decrypting(self,enc,key):
        enc = base64.b64decode(enc)
        print(enc)
        bl = bytes(key, "utf-8")
        iv = b'\x9a\x95\xb9\xe9#c\xd9\xa5\x92CG\xf9)\x0e\xf5x'
        cipher = AES.new(bl, AES.MODE_CBC, iv)
        return cipher.decrypt((enc))
