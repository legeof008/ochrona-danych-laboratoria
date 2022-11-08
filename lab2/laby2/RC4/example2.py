from Crypto.Cipher import ARC4
from odsiRC4.BruteForce import BruteForce
import os

key = b'klucz'
text = b'Idzie sasza sucha droga'
threshold = 0.8

cipher = ARC4.new(key)
enc = cipher.encrypt(text)
print(f'Encoded text: {enc}')
d = BruteForce(len(key), len(text), threshold, keys=[b'luksc', b'slucz', b'klucz', b'upczz'])

random_stuff = os.urandom(23)
random_distr = d.__frequency_of_bytes__(random_stuff)
random_entropy = d.__shannon__(random_distr)

print(f"Entropy of random bytes: {random_entropy}")

plain_distr = d.__frequency_of_bytes__(text)
plain_entropy = d.__shannon__(plain_distr)

enc_distr = d.__frequency_of_bytes__(enc)
enc_entropy = d.__shannon__(enc_distr)

print(f'Encoded enthropy: {enc_entropy}')
print(f'Plain text enthropy: {plain_entropy}')

# No wygląda na to im lepsza 'próba' (dłuższy tekst) tym większa różnica między
# entropią tekstu szyfrowanego, a zaszyfrowanym, lub entropią losowych bajcików.
# No ale zdarzały mi się, zwłaszcza dla małytch tekstów przypadki, gdzie klucz odkryty,
# wcale nie był prawidłowym, więc ten próg różnicy musi być umiejętnie dobrany.

guessed_key = d.brute_force_key(enc)
print(guessed_key)
