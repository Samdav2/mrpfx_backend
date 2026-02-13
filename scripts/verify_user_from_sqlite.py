#!/usr/bin/env python3
"""
Verify a WordPress user's password against the local SQLite `mrpfx.db`.

This script reads the `user_pass` for a given `user_email` (or `user_login`) from
the local SQLite database and verifies a provided plaintext password using the
project's `verify_password` implementation.

Usage:
  python scripts/verify_user_from_sqlite.py --email mrpfxworld@gmail.com --password '@Gratitude556' --db-path mrpfx.db

If `--password` is omitted the script will prompt for it interactively.
"""
import argparse
import sqlite3
import getpass
import sys
from typing import Optional

from app.core.security import verify_password


def fetch_user_pass(db_path: str, table: str, email: Optional[str] = None, login: Optional[str] = None):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        # Quote table name in case it starts with digits or contains unusual characters
        quoted_table = '"' + table.replace('"', '""') + '"'
        if email:
            cur.execute(f"SELECT ID, user_login, user_pass, user_email FROM {quoted_table} WHERE user_email=? LIMIT 1", (email,))
        else:
            cur.execute(f"SELECT ID, user_login, user_pass, user_email FROM {quoted_table} WHERE user_login=? LIMIT 1", (login,))

        row = cur.fetchone()
        return row
    finally:
        cur.close()
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Verify a user's password from the local SQLite WP DB")
    parser.add_argument('--email', help='User email to look up')
    parser.add_argument('--login', help='User login to look up (alternative)')
    parser.add_argument('--db-path', default='mrpfx.db', help='Path to SQLite DB file (default: mrpfx.db)')
    parser.add_argument('--table', default='8jH_users', help='Users table name (default: 8jH_users)')
    parser.add_argument('--password', help='Plaintext password to test (omit to prompt)')

    args = parser.parse_args()

    if not args.email and not args.login:
        print('Provide --email or --login to identify the user.')
        sys.exit(2)

    row = fetch_user_pass(args.db_path, args.table, email=args.email, login=args.login)
    if not row:
        print('User not found in the specified table/database.')
        sys.exit(3)

    print(f"Found user: ID={row['ID']} login={row['user_login']} email={row['user_email']}")
    stored_hash = row['user_pass']
    print(f"Stored hash (first 80 chars): {stored_hash[:80]}{'...' if len(stored_hash)>80 else ''}")

    plaintext = args.password
    if not plaintext:
        plaintext = getpass.getpass(prompt='Enter plaintext password to verify (input hidden): ')

    ok = verify_password(plaintext, stored_hash)
    if ok:
        print('MATCH: password verifies against stored hash')
        sys.exit(0)
    else:
        print('NO MATCH: password does NOT verify against stored hash')
        sys.exit(4)


if __name__ == '__main__':
    main()
