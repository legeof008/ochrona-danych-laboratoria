import hashlib

from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from client import Client


def hash_document_and_encrypt_with_private_key(document, key):
    hash_value = hashlib.sha256(document).hexdigest().encode("utf-8")
    cipher = PKCS1_OAEP.new(RSA.import_key(key))
    return cipher.encrypt(hash_value)


def encode_document(document, key):
    cipher = PKCS1_OAEP.new(RSA.import_key(key))
    return cipher.encrypt(document)


def verify_signature(signature, sender_pub_key, reciever_private_key):
    sig_1 = signature.split(b'STOP')[0]
    sig_2 = signature.split(b'STOP')[1]
    cipher = PKCS1_OAEP.new(RSA.import_key(reciever_private_key))
    doc = cipher.decrypt(sig_2)
    cipher = PKCS1_OAEP.new(RSA.import_key(sender_pub_key))
    hash_to_be_verified = cipher.decrypt(sig_1)
    counted_hash = hashlib.sha256(doc).hexdigest().encode("utf-8")
    if counted_hash == hash_to_be_verified:
        return True
    else:
        return False

def sign(message, priv_key):
    signer = PKCS1_v1_5.new(priv_key)
    digest = SHA256.new()
    digest.update(message)
    return signer.sign(digest)

def verify(message, signature, pub_key):
    signer = PKCS1_v1_5.new(pub_key)
    digest = SHA256.new()
    digest.update(message)
    return signer.verify(digest, signature)


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
    signature_part_1 = hash_document_and_encrypt_with_private_key(document, bob['public'])
    signature_part_2 = encode_document(document, alice['public'])
    msg = signature_part_1 + b"STOP" + signature_part_2
    c.send_binary_message("alice", msg)

    # Alice's POV
    signature = c.get_binary_message("alice")
    if verify_signature(signature, bob['private'], alice['private']):
        print("Bob is verified")
    else:
        print("Bob is not verified")
