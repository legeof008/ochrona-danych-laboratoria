from Crypto.Cipher import ARC4
import string
import itertools
from math import log2
from collections import Counter
import os


class BruteForce:
    def __init__(self, key_lenght, lenght_of_encrypted_message, threshold, keys=[]):
        ARC4.key_size = range(3, 257)
        self.threshold = threshold
        self.possible_keys_number = len(string.printable) ** key_lenght
        random_bytes = os.urandom(lenght_of_encrypted_message)
        random_distribiution = self.__frequency_of_bytes__(random_bytes)

        self.en_random = self.__shannon__(random_distribiution)
        if not keys:
            self.all_possible_keys = self.__generate_possible_keys__(key_lenght)
        else:
            self.all_possible_keys = keys

    def __generate_possible_keys__(self, key_lenght):
        return itertools.product(list(map(ord, list(string.printable))), repeat=key_lenght)

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

    def brute_force_key(self, ciphertext: bytes):
        i = 0
        possible_keys = []
        for key in self.all_possible_keys:
            if type(key) is bytes:
                cipher = ARC4.new(key)
            else:
                cipher = ARC4.new(bytes(list(key)))
            decrypted = cipher.decrypt(ciphertext)
            dec_frequency = self.__frequency_of_bytes__(decrypted)
            en_decoded = self.__shannon__(dec_frequency)
            if self.__key_guessed__(self.en_random, en_decoded, self.threshold):
                if type(key) is bytes:
                    possible_keys.append(key)
                else:
                    possible_keys.append(''.join(list(map(chr, list(key)))))

        return possible_keys
