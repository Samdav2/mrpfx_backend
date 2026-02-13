import asyncio
import sys
import os
from passlib.hash import phpass, bcrypt, md5_crypt
from passlib.hash import bcrypt as passlib_bcrypt

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def identify_user_hashes():
    # Hashes from the database
    hashes = {
        "mr.p": "$2b$2y$10$NNai6kvFe.wXHvZGF1Q7KuWSn8DRZ1V9h21zQH4onQgbu0M5r4Zdu",
        "adoxop1": "$wp$2y$10$LHYo7UVsQAuOjtnmcY53c.5tVd9Zu01Y1vwkH4IAJwcGnOuPnjh9q",
        "standard_wp": "$P$BW6SshU6Jre3M6A8u0yv/lKj.uQlyf/"
    }

    for name, h in hashes.items():
        print(f"\nUser: {name} | Hash: {h}")

        # 1. phpass
        try:
            if phpass.identify(h): print("  MATCH: phpass")
        except: pass

        # 2. bcrypt (generalized)
        try:
            # passlib's bcrypt handles $2a, $2b, $2y
            # But it might struggle with $wp$ or $2b$2y$ prefixes
            h_norm = h
            if h_norm.startswith("$wp$"): h_norm = "$" + h_norm[4:]
            if h_norm.startswith("$2b$2y$"): h_norm = "$" + h_norm[4:]

            if bcrypt.identify(h_norm): print(f"  MATCH: bcrypt (normalized to {h_norm[:10]}...)")
        except: pass

async def test_mrp_verification():
    # User: mr.p
    password = "@Gratitude55"
    db_hash = "$2b$2y$10$NNai6kvFe.wXHvZGF1Q7KuWSn8DRZ1V9h21zQH4onQgbu0M5r4Zdu"

    print(f"Target: mr.p | Password: {password}")

    # Prefix normalization for passlib:
    # 1. Strip $2b from $2b$2y$... to get $2y$...
    # 2. passlib_bcrypt.verify should handle $2y$ automatically
    v1 = "$" + db_hash[4:] # $2y$10$...

    print(f"Testing variation: {v1}")
    try:
        if passlib_bcrypt.verify(password, v1):
            print("  SUCCESS!")
        else:
            print("  FAILED")
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_mrp_verification())
