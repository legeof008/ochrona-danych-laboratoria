from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from client import Client


def encode_document(document, key):
    cipher = PKCS1_OAEP.new(RSA.import_key(key))
    return cipher.encrypt(document)


def sign(message, priv_key):
    signer = PKCS1_v1_5.new(RSA.importKey(priv_key))
    digest = SHA256.new()
    digest.update(message)
    return signer.sign(digest)


def verify(message, pub_key, priv_key):
    encoded_document = message.split(b'STOP')[0]
    sig = message.split(b'STOP')[1]
    true_message = PKCS1_OAEP.new(RSA.import_key(priv_key)).decrypt(encoded_document)
    signer = PKCS1_v1_5.new(RSA.importKey(pub_key))
    digest = SHA256.new()
    digest.update(true_message)
    return signer.verify(digest, sig)


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

    # Bob's POV
    document = b"ooo"
    alices_public_key = c.get_key('alice')
    encoded_doc = encode_document(document, alices_public_key)
    signature = sign(document, bob['private'])
    msg = encoded_doc + b"STOP" + signature
    c.send_binary_message("alice", msg)

    # Alice's POV
    message = c.get_binary_message("alice")
    bobs_public_key = c.get_key("bob")
    print()
    if verify(message, bobs_public_key, alice['private']):
        print("Bob is verified by Alice")
    else:
        print("Bob could not be verified by Alice")
