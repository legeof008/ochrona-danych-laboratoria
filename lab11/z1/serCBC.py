import ctypes
import multiprocessing
import time
from itertools import repeat

import numpy as numpy
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes


# zakłada, że a i b są bytes
def xor64(a, b):
    block = bytearray(a)
    for j in range(8):
        block[j] = a[j] ^ b[j]
    return bytes(block)


# zakłada, że key i plain_text są bytes
def encrypt_CBC_serial(key, plain_text):
    cipher_text = bytearray(plain_text)  # kopia! bytes -> bytearray
    des = DES.new(key, DES.MODE_CBC)
    for i in range(no_blocks):
        offset = i * block_size
        block = plain_text[offset:offset + block_size]
        encrypted = des.encrypt(block)
        cipher_text[offset:offset + block_size] = encrypted
    return bytes(cipher_text)  # bytearray -> bytes


# zakłada, że key i cipher_text są bytes
def decrypt_CBC_serial(key, cipher_text):
    plain_text = bytearray(cipher_text)
    des = DES.new(key, DES.MODE_CBC)
    for i in range(no_blocks):
        offset = i * block_size
        block = cipher_text[offset:offset + block_size]
        decrypted = des.decrypt(block)
        plain_text[offset:offset + block_size] = decrypted
    return bytes(plain_text)


def simple_decrypt(idx, cipher_block, block_size):
    des = DES.new(key, DES.MODE_CBC)
    decrypted = des.decrypt(cipher_block)
    for i in range(len(cipher_block)):
        shared_data[idx * block_size + i] = decrypted[i]


def decrypt_CBC_parallel(key, cipher_text, no_blocks):
    pool = multiprocessing.Pool(no_blocks)
    block_size = int(len(cipher_text) / no_blocks)
    blocks = []
    for i in range(no_blocks):
        offset = int(i * block_size)
        block = cipher_text[offset:offset + block_size]
        blocks.append(block)
    pool.starmap(simple_decrypt, zip(range(no_blocks), blocks, repeat(block_size)))


plain_text = b"alamakot" * 100000
key = b"haslo123"
iv = get_random_bytes(8)
block_size = 8
no_blocks = int(len(plain_text) / block_size)

starttime = time.time()
cipher_text = encrypt_CBC_serial(key, plain_text)
print('ECB Encrypt time serial: ', (time.time() - starttime))

starttime = time.time()
decrypted = decrypt_CBC_serial(key, cipher_text)
print('ECB Decrypt time serial: ', (time.time() - starttime))
print('...', decrypted[-15:-1])

# Moja implementacja
shared_data = multiprocessing.RawArray(ctypes.c_ubyte, plain_text)
starttime = time.time()
decrypt_CBC_parallel(key, cipher_text, 4)
endtime = time.time()
np_arr = numpy.frombuffer(shared_data, dtype=numpy.dtype(shared_data))

parallel_decrypted = "".join(list(map(chr, np_arr[0])))

print('ECB Decrypt time parallel: ', (endtime - starttime))
print('...', parallel_decrypted[-15:-1])

with open('ciphertext', 'wb') as f:
    f.write(cipher_text)
