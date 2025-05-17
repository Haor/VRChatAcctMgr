"""Crypto utilities for VRChat SecurePlayerPrefs."""
from __future__ import annotations

import base64
import hashlib
from Crypto.Cipher import DES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA1
import os

PASSWORD = b"vl9u1grTnvXA"
ITERATIONS = 1000
KEY_LEN = 8
IV_LEN = 8


def derive_key(iv: bytes) -> bytes:
    """Derive DES key from IV using PBKDF2."""
    return PBKDF2(PASSWORD, iv, dkLen=KEY_LEN, count=ITERATIONS, hmac_hash_module=SHA1)


def encrypt(plain: str) -> str:
    """Encrypt plaintext to Base64 string using VRChat's scheme."""
    iv = os.urandom(IV_LEN)
    key = derive_key(iv)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded = pad(plain.encode("utf-8"), DES.block_size)
    ct = cipher.encrypt(padded)
    blob = iv + ct
    return base64.b64encode(blob).decode("ascii")


def decrypt(b64_cipher: str) -> str:
    """Decrypt Base64 ciphertext."""
    blob = base64.b64decode(b64_cipher)
    iv, ct = blob[:IV_LEN], blob[IV_LEN:]
    key = derive_key(iv)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded = cipher.decrypt(ct)
    plain = unpad(padded, DES.block_size)
    return plain.decode("utf-8")


def md5_key(raw: str, index: int | None = None) -> str:
    """Return MD5 hash in upper case for registry key."""
    key = raw if index is None else f"{raw}{index}"
    return hashlib.md5(key.encode()).hexdigest().upper()

