from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from client import Client

if __name__ == '__main__':
    c = Client('http://localhost:2137')
    bob = {}
    alice = {}
    with open("alice", 'r') as key_file:
        alice['private'] = RSA.importKey(key_file.read()).exportKey()
    with open("alice.pub", 'r') as key_file:
        alice['public'] = RSA.importKey(key_file.read()).exportKey()
    with open("bob", 'r') as key_file:
        bob['private'] = RSA.importKey(key_file.read()).exportKey()
    with open("bob.pub", 'r') as key_file:
        bob['public'] = RSA.importKey(key_file.read()).exportKey()

    # Sending keys to server
    c.send_key("alice", alice['public'])
    c.send_key("bob", bob['public'])

    # Bob's POV sending message to Alice
    alices_key_bytes = c.get_key("alice")
    alices_key = RSA.import_key(alices_key_bytes)

    cipher = PKCS1_OAEP.new(alices_key)
    message = cipher.encrypt(b"anan")
    c.send_binary_message("alice", message)

    # Alice's pov recieving message
    bobs_msg = c.get_binary_message("alice")
    cipher = PKCS1_OAEP.new(RSA.import_key(alice['private']))
    bobs_msg_decrypted = cipher.decrypt(bobs_msg)
    print(bobs_msg_decrypted)