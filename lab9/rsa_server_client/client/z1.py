from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from client import Client

if __name__ == '__main__':
    c = Client('http://localhost:2137')

    deadbeef_bytes_key = c.get_key("deadbeef")
    deadbeef_key = RSA.import_key(deadbeef_bytes_key)

    cipher = PKCS1_OAEP.new(deadbeef_key)

    message = cipher.encrypt(b"oooook")
    c.send_binary_message("deadbeef", message)
