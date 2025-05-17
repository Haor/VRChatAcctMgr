from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from vrchataccountmanager.crypto_service import encrypt, decrypt

import os


def test_round_trip():
    for _ in range(100):
        plain = os.urandom(16).hex()
        cipher = encrypt(plain)
        assert decrypt(cipher) == plain

