import hashlib
import bcrypt
import pandas as pandas
from argon2 import PasswordHasher
import time

def md5_dictionary(dictionary):
    for password in dictionary:
        password = password.encode()
        hashed = hashlib.md5(password)
def sha256_dictionary(dictionary):
    for password in dictionary:
        password = password.encode()
        hashed = hashlib.sha256(password)


def bcrypt_dictionary(dictionary):
    for password in dictionary:
        password = password.encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())


def argon2_dictionary(dictionary):
    ph = PasswordHasher()
    for password in dictionary:
        password = password.encode()
        hashed = ph.hash(password)


if __name__ == '__main__':

    dictionary = pandas.read_csv("resources/passwords.csv", usecols=[0])['IMIĘ_PIERWSZE'].tolist()
    print(f"Number of passwords to hash: {len(dictionary)}")
    s1 = time.time()
    md5_dictionary(dictionary)
    e1 = time.time()
    t1 = (e1 - s1)/len(dictionary)
    print(f"Time for md5: {t1}")

    s2 = time.time()
    sha256_dictionary(dictionary)
    e2 = time.time()
    t2 = (e2 - s2)/len(dictionary)
    print(f"Time for sha256: {t2}")

    s3 = time.time()
    bcrypt_dictionary(dictionary[:1000])
    e3 = time.time()
    t3 = (e3 - s3)/1000
    print(f"Time for bcrypt: {t3}")

    s4 = time.time()
    argon2_dictionary(dictionary[:1000])
    e4 = time.time()
    t4 = (e4 - s4)/1000
    print(f"Time for argon2: {t4}")
