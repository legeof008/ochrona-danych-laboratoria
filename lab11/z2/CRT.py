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


# zakłada, że a i b są bytes
def xor64(a, b):
    block = bytearray(a)
    for j in range(8):
        block[j] = a[j] ^ b[j]
    return bytes(block)


# zakłada, że key i plain_text są bytes
def encrypt_CRT_serial(key, plain_text):
    cipher_text = bytearray(plain_text)  # kopia! bytes -> bytearray
    ctr = Counter.new(64, initial_value=0, prefix=b"")
    des = DES.new(key, DES.MODE_CTR, counter=ctr)
    for i in range(no_blocks):
        offset = i * block_size
        block = plain_text[offset:offset + block_size]
        encrypted = des.encrypt(block)
        cipher_text[offset:offset + block_size] = encrypted
    return bytes(cipher_text)  # bytearray -> bytes


# zakłada, że key i cipher_text są bytes
def decrypt_CRT_serial(key, cipher_text):
    plain_text = bytearray(cipher_text)
    ctr = Counter.new(64, initial_value=0, prefix=b"")
    des = DES.new(key, DES.MODE_CTR, counter=ctr)
    for i in range(no_blocks):
        offset = i * block_size
        block = cipher_text[offset:offset + block_size]
        decrypted = des.decrypt(block)
        plain_text[offset:offset + block_size] = decrypted
    return bytes(plain_text)


def simple_encrypt(idx, plaintext_block, block_size):
    ctr = Counter.new(64, initial_value=idx, prefix=b"")
    des = DES.new(key, DES.MODE_CTR, counter=ctr)
    decrypted = des.encrypt(plaintext_block)
    for i in range(len(plaintext_block)):
        shared_data_enc[idx * block_size + i] = decrypted[i]


def simple_decrypt(idx, cipher_block, block_size):
    ctr = Counter.new(64, initial_value=idx, prefix=b"")
    des = DES.new(key, DES.MODE_CTR, counter=ctr)
    decrypted = des.decrypt(cipher_block)
    for i in range(len(cipher_block)):
        shared_data[idx * block_size + i] = decrypted[i]


def encrypt_CRT_parallel(key, plaintext, no_blocks):
    pool = multiprocessing.Pool(no_blocks)
    block_size = int(len(plaintext) / no_blocks)
    blocks = []
    for i in range(no_blocks):
        offset = int(i * block_size)
        block = plaintext[offset:offset + block_size]
        blocks.append(block)
    pool.starmap(simple_encrypt, zip(range(no_blocks), blocks, repeat(block_size)))


def decrypt_CRT_parallel(key, cipher_text, no_blocks):
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
iv = get_random_bytes(200000)
block_size = 200000
no_blocks = int(len(plain_text) / block_size)

enc_times = []
dec_times = []

for threads in [1, 2, 4]:
    print(bcolors.WARNING + "With " + str(threads) + " threads :" + bcolors.ENDC)
    # Moja implementacja szyfrowanie
    shared_data_enc = multiprocessing.RawArray(ctypes.c_ubyte, plain_text)

    starttime = time.time()
    encrypt_CRT_parallel(key, plain_text, threads)
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
    decrypt_CRT_parallel(key, encrypted, threads)
    endtime = time.time()

    np_arr = numpy.frombuffer(shared_data, dtype=numpy.dtype(shared_data))

    parallel_decrypted = "".join(list(map(chr, np_arr[0])))

    print('CRT decrypt time parallel: ' + bcolors.OKGREEN + str(endtime - starttime) + bcolors.ENDC)
    print('...', parallel_decrypted[-15:-1])
    dec_times.append(endtime - starttime)

barWidth = 0.25
br1 = np.arange(3)
br2 = [x + barWidth for x in br1]

plt.bar(br1, enc_times, label="Encryption Times", width=barWidth)
plt.bar(br2, dec_times, label="Decryption Times", width=barWidth)

plt.xticks([r + barWidth for r in range(3)],
           ['1', '2', '4'])
plt.ylabel('Time')
plt.ylabel('Number of threads')
plt.legend()
plt.show()
