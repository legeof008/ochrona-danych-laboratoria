import ctypes
import multiprocessing
import time
from itertools import repeat

import numpy as numpy
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes


def xor64(a, b):
    block = bytearray(a)
    for j in range(len(b)):
        block[j] = a[j] ^ b[j]
    return bytes(block)


# zakłada, że key i plain_text są bytes
def encrypt_CBC_serial(key, plain_text, no_blocks):
    cipher_text = bytearray(plain_text)  # kopia! bytes -> bytearray
    des = DES.new(key, DES.MODE_ECB)
    block_size = int(len(cipher_text) / no_blocks)
    blocks = []
    for i in range(no_blocks):
        offset = int(i * block_size)
        block = cipher_text[offset:offset + block_size]
        blocks.append(block)
    for i in range(no_blocks):
        if i == 0:
            block = xor64(blocks[i], iv)
        else:
            block = xor64(blocks[i], blocks[i - 1])
        encrypted = des.encrypt(block)
        blocks[i] = encrypted
    return bytes(b"".join(blocks))  # bytearray -> bytes

def simple_decrypt(idx, cipher_block_former, cipher_block_current, block_size):
    des = DES.new(key, DES.MODE_ECB)
    decrypted = des.decrypt(cipher_block_current)
    plain_text = xor64(cipher_block_former, decrypted)
    for i in range(len(cipher_block_current)):
        shared_data[idx * block_size + i] = plain_text[i]


def decrypt_CBC_parallel(key, cipher_text, no_blocks):
    pool = multiprocessing.Pool(no_blocks)
    block_size = int(len(cipher_text) / no_blocks)
    blocks = []
    former_blocs = []
    for i in range(no_blocks):
        offset = int(i * block_size)
        block = cipher_text[offset:offset + block_size]
        if i == 0:
            former_blocs.append(iv)
        else:
            former_blocs.append(blocks[i - 1])
        blocks.append(block)
    pool.starmap(simple_decrypt, zip(range(no_blocks), former_blocs, blocks, repeat(block_size)))


plain_text = b"alamakot" * 100000
key = b"haslo123"
block_size = 200000
iv = get_random_bytes(block_size)
no_blocks = int(len(plain_text) / block_size)

starttime = time.time()
cipher_text = encrypt_CBC_serial(key, plain_text, no_blocks)
print('CBC Encrypt time serial: ', (time.time() - starttime))

# Moja implementacja
shared_data = multiprocessing.RawArray(ctypes.c_ubyte, plain_text)
starttime = time.time()
decrypt_CBC_parallel(key, cipher_text, no_blocks)
endtime = time.time()
np_arr = numpy.frombuffer(shared_data, dtype=numpy.dtype(shared_data))

parallel_decrypted = "".join(list(map(chr, np_arr[0])))

print('CBC Decrypt time parallel: ', (endtime - starttime))
print('...', parallel_decrypted[-15:-1])

with open('ciphertext', 'wb') as f:
    f.write(cipher_text)
