import asyncio
import sys
import os
import bcrypt
import hashlib
from passlib.hash import bcrypt as passlib_bcrypt

async def md5_bcrypt_debug():
    password = "@Gratitude55"
    db_hash = "$2b$2y$10$NNai6kvFe.wXHvZGF1Q7KuWSn8DRZ1V9h21zQH4onQgbu0M5r4Zdu"

    # Normalize hash
    normalized_hash = db_hash
    if normalized_hash.startswith("$2b$2y$"):
        normalized_hash = "$" + normalized_hash[4:]
    elif normalized_hash.startswith("$wp$"):
        normalized_hash = "$" + normalized_hash[4:]

    print(f"Target: mr.p | Password: {password}")
    print(f"Normalized Hash: {normalized_hash}\n")

    # 1. Plain
    try:
        if passlib_bcrypt.verify(password, normalized_hash):
            print("SUCCESS: Plain password matched!")
            return
    except: pass

    # 2. MD5 pre-hash
    md5_pass = hashlib.md5(password.encode()).hexdigest()
    print(f"Testing MD5 pre-hash: {md5_pass}")
    try:
        if passlib_bcrypt.verify(md5_pass, normalized_hash):
            print("SUCCESS: MD5 pre-hash matched!")
            return
    except: pass

    # 3. MD5 pre-hash (binary/raw) - less common but possible
    md5_raw = hashlib.md5(password.encode()).digest()
    # No, bcrypt expects a string or bytes of the string.

    print("\nNeither plain nor MD5 pre-hash matched.")

if __name__ == "__main__":
    asyncio.run(md5_bcrypt_debug())
