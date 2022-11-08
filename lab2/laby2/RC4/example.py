from odsiRC4 import RC4
first = RC4.RC4()

key = "klucz"
password = "Idzie sasza sucha droga"

encrypted = first.encrypt(key, password)
encrypted_str = ''.join(list(map(chr, encrypted)))

decrypted = first.decrypt(key, encrypted_str)
decrypted_str = ''.join(list(map(chr, decrypted)))

print("Original text: ")
print(password)
print("Encrypted text: ")
print(encrypted_str)
print("Decrypted text:")
print(decrypted_str)
