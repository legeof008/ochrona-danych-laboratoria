from Crypto.Cipher import ARC4, AES
from Crypto.Protocol.KDF import PBKDF2
import string
import itertools
from math import log2
from collections import Counter
import os


class BruteForce:
    def __init__(self, key_lenght, iv, threshold, keys=[]):
        ARC4.key_size = range(3, 257)
        self.threshold = threshold
        self.iv = iv
        if not keys:
            self.all_possible_keys = self.__generate_possible_keys__(key_lenght)
        else:
            self.all_possible_keys = keys

    def __generate_possible_keys__(self, key_lenght):
        return itertools.product(list(string.ascii_letters), repeat=key_lenght)

    def __frequency_of_bytes__(self, bytes):
        occurances = Counter(list(bytes))
        for word in occurances:
            occurances[word] = occurances[word] / len(bytes)
        return occurances

    def __shannon__(self, frequency):
        total = sum(frequency.values())
        return sum(freq / total * log2(total / freq) for freq in frequency.values())

    def __key_guessed__(self, en_random, en_decoded, threshold):
        if abs(en_decoded - en_random) > threshold:
            return True
        else:
            return False

    def __key_guessed_static__(self,en_decoded):
        if en_decoded < self.threshold:
            return True
        else:
            return False

    def brute_force_key(self, directory):
        i = 0
        possible_keys = []
        self.__load__file__(directory)
        for key in self.all_possible_keys:
            print(f"Trying: {''.join(key)}")
            print(f"Found: {len(possible_keys)}")
            passw = PBKDF2(''.join(key), b"abc")
            cbc = AES.new(passw, AES.MODE_CBC, self.iv)
            decrypted = cbc.decrypt(self.body)
            dec_frequency = self.__frequency_of_bytes__(decrypted)
            en_decoded = self.__shannon__(dec_frequency)
            if self.__key_guessed_static__(en_decoded):
                possible_keys.append(key)
            _ = os.system('clear')
        return possible_keys

    def brute_force_GENkey(self, directory):
        i = 0
        possible_keys = []
        self.__load__file__(directory)
        for key in self.all_possible_keys:
            print(f"Trying: {''.join(key)}")
            print(f"Found: {len(possible_keys)}")
            passw = PBKDF2(''.join(key), b"abc")
            cbc = AES.new(passw, AES.MODE_CBC, self.iv)

            diff = 16 - (len(self.header) % 16)
            padding = bytearray(b'0' * diff)
            self.header.extend(padding)

            decrypted = cbc.decrypt(self.header)
            dec_frequency = self.__frequency_of_bytes__(decrypted)
            en_decoded = self.__shannon__(dec_frequency)
            if self.__key_guessed_static__(en_decoded):
                possible_keys.append(key)
            _ = os.system('clear')
        return possible_keys

    def __load__file__(self, directory):

        file = open(directory, "rb")
        img_bytes = bytearray(file.read())

        self.header = img_bytes[:53]
        self.body = img_bytes[54:]
        self.img_bytes=img_bytes

        random_bytes = os.urandom(len(self.body))
        random_distribiution = self.__frequency_of_bytes__(random_bytes)
        self.en_random = self.__shannon__(random_distribiution)


if __name__ == "__main__":
    br = BruteForce(3, bytes(list(map(ord, list("a" * 16)))), 2.5)
    keys = br.brute_force_GENkey("resources/we800_CBC_encrypted_full.bmp")
    print(keys)
    for key in keys:
        passw = PBKDF2(''.join(key), b"abc")
        cbc = AES.new(passw, AES.MODE_CBC,  bytes(list(map(ord, list("a" * 16)))))
        diff = 16 - (len(br.img_bytes) % 16)
        padding = bytearray(b'0' * diff)
        br.img_bytes.extend(padding)
        decrypted = cbc.decrypt(br.img_bytes)
        f = open("outputs/brute_force_" + key + ".bmp", 'wb')
        f.write(decrypted)
        f.close()
