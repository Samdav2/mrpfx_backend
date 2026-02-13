#!/usr/bin/env python3
"""
Simple helper to verify a plaintext password against a WordPress-stored hash
using the project's `verify_password` function.

Usage:
 1) Get the stored hash from your WP DB (see instructions below).
 2) Run:
    python scripts/test_verify_password.py --password 'PASTE_PASSWORD' --hash 'PASTE_HASH'

You should run this from the project root with your virtualenv activated so
`app` package imports resolve.
"""
import argparse
import sys

from app.core.security import verify_password


def main():
    parser = argparse.ArgumentParser(description="Verify plaintext vs WP stored hash")
    parser.add_argument("--password", "-p", required=True, help="Plaintext password to test")
    parser.add_argument("--hash", "-s", required=False, help="Stored hash from DB (user_pass)")
    args = parser.parse_args()

    stored_hash = args.hash
    if not stored_hash:
        try:
            stored_hash = input("Paste stored user_pass hash from DB: ").strip()
        except KeyboardInterrupt:
            print("\nAborted")
            sys.exit(1)

    ok = verify_password(args.password, stored_hash)
    if ok:
        print("MATCH: password verifies against stored hash")
        sys.exit(0)
    else:
        print("NO MATCH: password does NOT verify against stored hash")
        sys.exit(2)


if __name__ == "__main__":
    main()
