import asyncio
import sys
import os
from passlib.hash import phpass, bcrypt, md5_crypt

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import select
from app.db.session import AsyncSession, engine
from app.model.wordpress.core import WPUser

async def identify_hashes():
    async with AsyncSession(engine) as session:
        statement = select(WPUser)
        results = await session.execute(statement)
        users = results.scalars().all()

        for u in users:
            h = u.user_pass
            print(f"\nID={u.ID} | Login={u.user_login} | Hash={h}")

            # Try to identify
            matches = []

            # 1. phpass
            try:
                if phpass.identify(h): matches.append("phpass")
            except: pass

            # 2. bcrypt
            try:
                # passlib's bcrypt is strict about prefixes, let's try with normalization
                h_norm = h
                if h_norm.startswith("$wp$"): h_norm = "$" + h_norm[4:]
                if h_norm.startswith("$2b$2y$"): h_norm = "$" + h_norm[4:]

                if bcrypt.identify(h_norm): matches.append("bcrypt")
            except: pass

            # 3. MD5
            if len(h) == 32: matches.append("plain_md5")

            print(f"  Identified as: {matches}")

if __name__ == "__main__":
    asyncio.run(identify_hashes())
