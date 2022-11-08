import unittest
from Crypto.Cipher import ARC4
from ..BruteForce import BruteForce


class BruteForceImplementation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        ARC4.key_size = range(3, 257)

        cls.key = b'klucz'
        text = b'Idzie sasza sucha droga'
        threshold = 0.8

        cipher = ARC4.new(cls.key)
        cls.enc = cipher.encrypt(text)

        cls.d = BruteForce(len(cls.key), len(text), threshold, keys=[b'luksc', b'slucz', b'klucz', b'upczz'])

    def test_correct_key(self):
        self.assertEqual(self.d.brute_force_key(self.enc)[0], self.key)
