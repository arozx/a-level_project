import unittest
from password import hash_password
from passlib.hash import pbkdf2_sha256


class TestPassword(unittest.TestCase):
    def test_hash_password(self):
        # Test hashing a password
        password = "password123"
        hashed_password = hash_password(password)
        self.assertTrue(pbkdf2_sha256.verify(password, hashed_password))


if __name__ == "__main__":
    unittest.main()
