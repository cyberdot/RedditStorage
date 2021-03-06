import hashlib
import os
import base64

from Crypto.Cipher import AES
from Crypto import Random

class AESCipher:
    
    def __init__(self, key):
        #self.bs = 32
        self.key = hashlib.sha256(key).digest() #turns the password into a 32char long key
    
        #need to make our string divisible by 16 for AES encryption
    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
        
        #encrypts plaintext and generates IV (initialization vector)
    def encrypt(self, plaintext):
        plaintext = self.pad(plaintext)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(plaintext)

        #derypts ciphertexts
    def decrypt(self, ciphertext):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")
    
        #encrypts a file and returns a comment to be posted
    def encrypt_file(self, file_path):

        with open(file_path, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext)
        comment = base64.b64encode(enc)
        #comment = enc.decode('ISO-8859-1').encode('ascii')
        return comment 
        
        #takes in a comment to be posted and decrypts it into a file
    def decrypt_file(self, comment, file_path):

        ciphertext = base64.b64decode(comment)
        #ciphertext = comment.decode('ascii').encode('ISO-8859-1')
        dec = self.decrypt(ciphertext)
        with open(file_path, 'wb') as fo:
            fo.write(dec)

"""
example:

cipher1 = AESCipher(KEYPASS)

print cipher1.key

encryption = cipher1.encrypt_file("gogo.txt")

#decryption = cipher1.decrypt(encryption)

dog = base64.b64encode(encryption)
print dog
print "hello this is bad"
print base64.b64decode(dog)

"""
