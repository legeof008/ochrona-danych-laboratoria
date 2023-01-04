import ctypes
import multiprocessing
import time
from itertools import repeat

import matplotlib.pyplot as plt
import numpy as np
import numpy as numpy
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def xor64(a, b):
    block = bytearray(a)
    for j in range(len(b)):
        block[j] = a[j] ^ b[j]
    return bytes(block)

def simple_encrypt(idx, plaintext_block, block_size, nonce):
    des = DES.new(key, DES.MODE_ECB)
    encrypted = des.encrypt(xor64(nonce, idx.to_bytes(len(nonce),'big')))
    ciphertext = xor64(encrypted, plaintext_block)
    for i in range(len(plaintext_block)):
        shared_data_enc[idx * block_size + i] = ciphertext[i]


def simple_decrypt(idx, cipher_block, block_size, nonce):
    des = DES.new(key, DES.MODE_ECB)
    decrypted = des.encrypt(xor64(nonce, idx.to_bytes(len(nonce),'big')))
    plain_text = xor64(cipher_block, decrypted)
    for i in range(len(cipher_block)):
        shared_data[idx * block_size + i] = plain_text[i]


def encrypt_CRT_parallel(nonce, plaintext, no_blocks):
    pool = multiprocessing.Pool(no_blocks)
    block_size = int(len(plaintext) / no_blocks)
    blocks = []
    for i in range(no_blocks):
        offset = int(i * block_size)
        block = plaintext[offset:offset + block_size]
        blocks.append(block)
    pool.starmap(simple_encrypt, zip(range(no_blocks), blocks, repeat(block_size), repeat(nonce)))


def decrypt_CRT_parallel(nonce, cipher_text, no_blocks):
    pool = multiprocessing.Pool(no_blocks)
    block_size = int(len(cipher_text) / no_blocks)
    blocks = []
    for i in range(no_blocks):
        offset = int(i * block_size)
        block = cipher_text[offset:offset + block_size]
        blocks.append(block)
    pool.starmap(simple_decrypt, zip(range(no_blocks), blocks, repeat(block_size), repeat(nonce)))


plain_text = b"alamakot" * 100000
key = b"haslo123"
enc_times = []
dec_times = []

for threads in [1, 2, 4]:
    print(bcolors.WARNING + "With " + str(threads) + " threads :" + bcolors.ENDC)
    # Moja implementacja szyfrowanie
    shared_data_enc = multiprocessing.RawArray(ctypes.c_ubyte, plain_text)
    no_blocks = threads
    block_size = int(len(plain_text) / no_blocks)
    nonce = get_random_bytes(block_size)

    starttime = time.time()
    encrypt_CRT_parallel(nonce, plain_text, threads)
    endtime = time.time()

    np_arr = numpy.frombuffer(shared_data_enc, dtype=numpy.dtype(shared_data_enc))
    encrypted = []

    for i in range(len(np_arr[0])):
        encrypted.append(np_arr[0][i].tobytes())

    encrypted = b"".join(encrypted)

    print('CRT encrypt time parallel: ' + bcolors.OKGREEN + str(endtime - starttime) + bcolors.ENDC)
    print('...', encrypted[-15:-1])
    enc_times.append(endtime - starttime)

    # Moja implementacja deszyfrowanie
    shared_data = multiprocessing.RawArray(ctypes.c_ubyte, plain_text)

    starttime = time.time()
    decrypt_CRT_parallel(nonce, encrypted, threads)
    endtime = time.time()

    np_arr = numpy.frombuffer(shared_data, dtype=numpy.dtype(shared_data))

    parallel_decrypted = "".join(list(map(chr, np_arr[0])))

    print('CRT decrypt time parallel: ' + bcolors.OKGREEN + str(endtime - starttime) + bcolors.ENDC)
    print('...', parallel_decrypted[-15:-1])
    dec_times.append(endtime - starttime)