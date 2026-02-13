import asyncio
import sys
import os
import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def advanced_debug():
    # User: mr.p
    password = "@Gratitude55"
    db_hash = "$2b$2y$10$NNai6kvFe.wXHvZGF1Q7KuWSn8DRZ1V9h21zQH4onQgbu0M5r4Zdu"

    print(f"Target: mr.p | Password: {password}")
    print(f"DB Hash: {db_hash}\n")

    variations = [
        db_hash,
        "$" + db_hash[4:],         # Strip $2b$ or $wp$ -> $2y$...
        "$2b$" + db_hash[7:],      # Replace $2b$2y$10$ with $2b$10$
        "$2y$" + db_hash[7:],      # Replace $2b$2y$10$ with $2y$10$
        "$2a$" + db_hash[7:],      # Replace $2b$2y$10$ with $2a$10$
        db_hash[3:],               # Just strip $2b -> $2y$10...
    ]

    for v in variations:
        print(f"Testing variation: {v}")

        # 1. Raw bcrypt
        check_v = v
        if check_v.startswith("$2y$"):
            check_v = "$2b$" + check_v[4:]

        try:
            if bcrypt.checkpw(password.encode(), check_v.encode()):
                print(f"  FAILED (matched!) but how? logic says it should return true. Wait, I mean SUCCESS!")
                return
        except:
            pass

        # 2. Passlib (more forgiving)
        try:
            if passlib_bcrypt.verify(password, v):
                print(f"  SUCCESS (passlib) with: {v}")
                return
        except:
            pass

    print("\nNo variations matched. Checking for character encoding issues...")
    # Try common variations of the password? No, user is sure.

if __name__ == "__main__":
    asyncio.run(advanced_debug())
