#!/usr/bin/env python3
"""
Fetch a WordPress user's `user_pass` from the database and verify a plaintext
password using the project's WordPress-compatible verifier.

Notes:
- This script uses `pymysql` for MySQL/MariaDB connections. Install with:
    pip install pymysql
- You can provide DB credentials via command-line args or environment variables.
- For safety, avoid passing plaintext passwords on the command line; use the
  interactive prompt instead.

Usage examples:
  # Interactive (recommended): prompts for DB credentials and password
  python scripts/verify_user_from_db.py --email mrpfxworld@gmail.com

  # Provide DB credentials via args (still recommended to enter password interactively)
  python scripts/verify_user_from_db.py --email mrpfxworld@gmail.com \
      --db-host localhost --db-user wpuser --db-password 'secret' --db-name wp_db --table wp_users

"""
import argparse
import getpass
import os
import sys

try:
    import pymysql
except Exception:
    print("pymysql is required but not installed. Install with: pip install pymysql")
    sys.exit(2)

from app.core.security import verify_password


def fetch_user_pass(conn, table, email=None, login=None):
    cur = conn.cursor()
    if email:
        sql = f"SELECT ID,user_login,user_pass,user_email FROM `{table}` WHERE user_email=%s LIMIT 1"
        cur.execute(sql, (email,))
    else:
        sql = f"SELECT ID,user_login,user_pass,user_email FROM `{table}` WHERE user_login=%s LIMIT 1"
        cur.execute(sql, (login,))

    row = cur.fetchone()
    cur.close()
    return row


def main():
    parser = argparse.ArgumentParser(description="Verify a user's password from the DB using WordPress-compatible hashing")
    parser.add_argument("--email", help="User email to look up")
    parser.add_argument("--login", help="User login to look up (alternative to --email)")
    parser.add_argument("--db-host", default=os.environ.get("DB_HOST", "localhost"))
    parser.add_argument("--db-port", type=int, default=int(os.environ.get("DB_PORT", 3306)))
    parser.add_argument("--db-user", default=os.environ.get("DB_USER", "root"))
    parser.add_argument("--db-password", default=os.environ.get("DB_PASSWORD"))
    parser.add_argument("--db-name", default=os.environ.get("DB_NAME"))
    parser.add_argument("--table", default=os.environ.get("WP_USERS_TABLE", "8jH_users"), help="Users table name (default: 8jH_users)")
    parser.add_argument("--password", help="Plaintext password to test (not recommended on CLI)")

    args = parser.parse_args()

    if not args.email and not args.login:
        print("Provide --email or --login to identify the user.")
        sys.exit(2)

    if not args.db_name:
        print("Provide database name via --db-name or DB_NAME environment variable.")
        sys.exit(2)

    db_password = args.db_password
    if db_password is None:
        db_password = getpass.getpass(prompt=f"DB password for {args.db_user}@{args.db_host}: ")

    try:
        conn = pymysql.connect(
            host=args.db_host,
            port=args.db_port,
            user=args.db_user,
            password=db_password,
            database=args.db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )
    except Exception as e:
        print(f"Failed to connect to DB: {e}")
        sys.exit(3)

    try:
        row = fetch_user_pass(conn, args.table, email=args.email, login=args.login)
        if not row:
            print("User not found in the specified table.")
            sys.exit(4)

        print(f"Found user: ID={row['ID']} login={row['user_login']} email={row['user_email']}")
        stored_hash = row['user_pass']
        print(f"Stored hash (first 60 chars): {stored_hash[:60]}{'...' if len(stored_hash)>60 else ''}")

        plaintext = args.password
        if not plaintext:
            plaintext = getpass.getpass(prompt="Enter plaintext password to verify (input hidden): ")

        ok = verify_password(plaintext, stored_hash)
        if ok:
            print("MATCH: password verifies against stored hash")
            sys.exit(0)
        else:
            print("NO MATCH: password does NOT verify against stored hash")
            sys.exit(5)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
