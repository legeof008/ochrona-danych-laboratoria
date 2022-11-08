from math import log2
from collections import Counter


def __frequency_of_bytes__(bytes):
    occurances = Counter(list(bytes))
    for word in occurances:
        occurances[word] = occurances[word] / len(bytes)
    return occurances


def __shannon__(frequency):
    total = sum(frequency.values())
    return sum(freq / total * log2(total / freq) for freq in frequency.values())


def count_entropy_of_bytes(input_bytes):
    frequency = __frequency_of_bytes__(input_bytes)
    return __shannon__(frequency)
