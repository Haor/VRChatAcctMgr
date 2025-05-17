#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decode VRChat SDK SecurePlayerPrefs stored in Windows registry.
Author : ChatGPT (o3)
"""

import re
import binascii
import hashlib
import base64
import argparse
from pathlib import Path
from typing import Dict

from Crypto.Cipher import DES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA1

# ------------------------------------------------------------------ #
#               Constants matching VRChat SDK internals              #
# ------------------------------------------------------------------ #
PASSWORD   = b"vl9u1grTnvXA"   # hard-coded in ApiCredentials
IV_SIZE    = 8                 # bytes
KEY_SIZE   = 8                 # DES key size
ITERATIONS = 1000              # PBKDF2 rounds

# SDK original (raw) keys → their MD5 representation in registry
ORIGINAL_KEYS = [
    "authTokenProvider",
    "authTokenProviderUserId",
    "authToken",
    "twoFactorAuthToken",
    "humanName",
    "username",
    "password",
]
MD5_LOOKUP = {hashlib.md5(k.encode()).hexdigest().upper(): k for k in ORIGINAL_KEYS}

# ------------------------------------------------------------------ #
#                         Registry parsing                           #
# ------------------------------------------------------------------ #
REG_HEX_LINE = re.compile(r'"([^"]+)"=hex:(.*)', re.I)

def parse_reg_file(path: Path) -> Dict[str, Dict[str, str]]:
    """
    Parse a .reg file exported from Windows registry editor.
    Returns { registry_path : { pref_key : raw_hex_string } }.
    Handles multi-line hex values (lines ending with '\').
    """
    data: Dict[str, Dict[str, str]] = {}
    current_path = None
    hex_key, hex_buf = None, []

    # .reg files exported by regedit are UTF-16 LE with BOM.
    with path.open("r", encoding="utf-16le") as fh:
        for raw_line in fh:
            line = raw_line.rstrip("\r\n")

            # Continuation of a multi-line hex value
            if hex_key is not None:
                continued = line.lstrip()
                hex_buf.append(continued)
                if not continued.endswith("\\"):
                    joined = "".join(hex_buf).rstrip("\\")
                    data[current_path][hex_key] = joined
                    hex_key, hex_buf = None, []
                continue

            # New registry section
            if line.startswith("[") and line.endswith("]"):
                current_path = line.strip("[]")
                data.setdefault(current_path, {})
                continue

            # Key = hex:...
            m = REG_HEX_LINE.match(line)
            if m:
                hex_key, first_part = m.groups()
                if first_part.endswith("\\"):
                    hex_buf = [first_part[:-1]]
                else:
                    data[current_path][hex_key] = first_part
                continue

    return data

# ------------------------------------------------------------------ #
#                          Decryption                                #
# ------------------------------------------------------------------ #
def decrypt_pref(hex_string: str) -> str:
    """
    Convert comma-separated hex string to plaintext.
    Registry stores bytes like 44,52,6c,...,00
    1. Strip non-hex chars and unhexlify
    2. Remove trailing NULL
    3. Base64-decode → [IV | ciphertext]
    4. PBKDF2(PASSWORD, IV) → DES key
    5. DES-CBC decrypt + PKCS7 unpad
    """
    # Remove commas / whitespace / backslashes
    clean_hex = "".join(ch for ch in hex_string if ch in "0123456789abcdefABCDEF")
    blob = binascii.unhexlify(clean_hex)

    # C-string → drop trailing NULLs
    b64_encoded = blob.rstrip(b"\0").decode("ascii")
    full_blob   = base64.b64decode(b64_encoded)

    iv, ct = full_blob[:IV_SIZE], full_blob[IV_SIZE:]
    key = PBKDF2(PASSWORD, iv, dkLen=KEY_SIZE, count=ITERATIONS, hmac_hash_module=SHA1)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded = cipher.decrypt(ct)

    pad_len = padded[-1]
    if pad_len < 1 or pad_len > DES.block_size:
        raise ValueError("Invalid PKCS7 padding")
    return padded[:-pad_len].decode("utf-8", errors="replace")

# ------------------------------------------------------------------ #
#                          CLI / Demo                                #
# ------------------------------------------------------------------ #
def main():
    parser = argparse.ArgumentParser(
        description="Decode VRChat SDK SecurePlayerPrefs from .reg export"
    )
    parser.add_argument("regfile", help="Path to .reg file exported from Windows registry")
    args = parser.parse_args()

    reg_path = Path(args.regfile).expanduser()
    if not reg_path.is_file():
        parser.error(f"File not found: {reg_path}")

    prefs = parse_reg_file(reg_path)

    print("\n=== Decryption Result ===")
    for hive_path, kv in prefs.items():
        # Focus on UnityEditor/DefaultCompany but you may relax this filter
        if "UnityEditor" not in hive_path or "DefaultCompany" not in hive_path:
            continue

        project = hive_path.split("\\")[-1]
        print(f"\n[{project}] — {hive_path}")

        for full_key, hex_val in kv.items():
            # Skip UnityGraphicsQuality, dword values etc.
            if "_h" not in full_key:
                continue

            md5_part = full_key.split("_h")[0]
            original = MD5_LOOKUP.get(md5_part, "unknown")

            try:
                plain = decrypt_pref(hex_val)
                print(f" • {original:<25} ({full_key})")
                print(f"   → {plain}")
            except Exception as e:
                print(f" • {original:<25} ({full_key})")
                print(f"   !! decrypt error: {e}")

if __name__ == "__main__":
    main()