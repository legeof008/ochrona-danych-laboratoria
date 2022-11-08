import hashlib
import random
import string


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def completed_generation(texts, byte_array_1, byte_array_2):
    if byte_array_1 == byte_array_2:
        return False
    h1 = hashlib.sha256(byte_array_1.encode()).hexdigest()
    h2 = hashlib.sha256(byte_array_2.encode()).hexdigest()
    if h1[0:10] == h2[0:10]:
        texts.append([[h1, byte_array_1], [h2, byte_array_2]])
        return True
    else:
        return False


r1 = get_random_string(10)
r2 = get_random_string(10)
texts = []
while not completed_generation(texts, r1, r2):
    r1 = get_random_string(10)
    r2 = get_random_string(10)

print(texts)
