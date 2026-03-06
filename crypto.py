from Crypto.Cipher import AES
from Crypto.Util import Counter
from hashlib import md5

class AESCipher:
    def __init__(self, passphrase):
        # Derive a 16-byte key from the passphrase
        self.key = md5(passphrase.encode('utf-8')).digest()

    def encrypt(self, plaintext):
        # Create a counter for CTR mode
        ctr = Counter.new(128)
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        return cipher.encrypt(plaintext.encode('utf-8'))

    def decrypt(self, ciphertext):
        ctr = Counter.new(128)
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        return cipher.decrypt(ciphertext).decode('utf-8')

# Example usage:
# passphrase = 'my_shared_passphrase'
# cipher = AESCipher(passphrase)
# ciphertext = cipher.encrypt('Hello, World!')
# plaintext = cipher.decrypt(ciphertext)
