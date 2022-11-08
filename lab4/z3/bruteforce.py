from argon2 import PasswordHasher
import itertools
import string
import os

def generate_possible_keys(key_lenght):
    return itertools.product(string.ascii_lowercase, repeat=key_lenght)


target = "$argon2id$v=19$m=65536,t=3,p=4$4Vzr3bvXWuvdmzMG4PxfCw$NWNunMWdo0ugkWWsL8Z+sdMKnDcJp0vDfMkr30Lmpd4"
passwords = generate_possible_keys(2)

targets = []
ps = PasswordHasher()
for password in passwords:
    try:
        print(f"Trying: {''.join(password)}")
        if ps.verify(target, "".join(password)):
            targets.append(''.join(password))
    except:
        os.system("clear")
print(targets)
