import unittest
from Crypto.Cipher import ARC4
from ..RC4 import RC4


class TestRC4Implementation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        ARC4.key_size = range(3, 257)
        cls.key_1 = "klucz"
        cls.password_1 = "idzie sasza sucha droga"

        cls.key_2 = b'klucz'
        cls.password_2 = b'idzie sasza sucha droga'

        cls.algorithm = RC4()

        cls.e1 = ARC4.new(cls.key_2)
        cls.e2 = ARC4.new(cls.key_2)

        cls.encrypted_1 = cls.algorithm.encrypt(cls.key_1, cls.password_1)
        cls.encrypted_str = ''.join(list(map(chr, cls.encrypted_1)))
        cls.decrypted_1 = cls.algorithm.decrypt(cls.key_1, cls.encrypted_str)

        cls.encrypted_2 = cls.e1.encrypt(cls.password_2)
        cls.decrypted_2 = cls.e2.decrypt(cls.encrypted_2)

    def test_if_no_mistake_was_made_with_input_data(self):
        self.assertEqual(list(self.password_2), list(map(ord, list(self.password_1))))
        self.assertEqual(list(self.key_2), list(map(ord, list(self.key_1))))

    def test_encryption(self):
        self.assertEqual(''.join(list(map(chr, self.decrypted_1))), self.password_1)
        self.assertEqual(self.encrypted_1, list(self.encrypted_2))

    def test_decryption(self):
        self.assertEqual(self.decrypted_1, list(self.decrypted_2))
        self.assertEqual(self.decrypted_1, list(map(ord, list(self.password_1))))
