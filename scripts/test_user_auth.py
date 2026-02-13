import asyncio
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import select
from app.db.session import AsyncSession, engine
from app.model.wordpress.core import WPUser
from app.core.security import verify_password

from passlib.hash import bcrypt as passlib_bcrypt

async def test_passlib_verification():
    tests = [
        {"login": "mr.p", "password": "@Gratitude55", "hash": "$2b$2y$10$NNai6kvFe.wXHvZGF1Q7KuWSn8DRZ1V9h21zQH4onQgbu0M5r4Zdu"},
        {"login": "adoxop1gmail-com", "password": "Encrypted@103", "hash": "$wp$2y$10$LHYo7UVsQAuOjtnmcY53c.5tVd9Zu01Y1vwkH4IAJwcGnOuPnjh9q"}
    ]

    for t in tests:
        print(f"\nTesting User: {t['login']}")
        h = t['hash']

        # Passlib handles $2y$ and $wp$ much better if we strip the $wp$ prefix
        if h.startswith("$wp$"): h = "$" + h[4:]
        if h.startswith("$2b$2y$"): h = "$" + h[4:] # Try stripping $2b

        try:
            ok = passlib_bcrypt.verify(t['password'], h)
            print(f"  Result: {'SUCCESS' if ok else 'FAILED'}")

            if not ok:
                # Try raw if strip failed
                h_raw = t['hash']
                if h_raw.startswith("$wp$"): h_raw = h_raw[3:] # Try stripping just the prefix
                print(f"  Trying again with raw/alt strip: {h_raw}")
                ok_alt = passlib_bcrypt.verify(t['password'], h_raw)
                print(f"  Result (Alt): {'SUCCESS' if ok_alt else 'FAILED'}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_passlib_verification())
