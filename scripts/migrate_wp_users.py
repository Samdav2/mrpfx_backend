import asyncio
import re
import sys
import os
from datetime import datetime
from typing import List, Dict, Optional

# Add the project root to the python path
sys.path.append(os.getcwd())

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import engine, ini_db
from app.model.user import User


def parse_sql_value(value: str) -> str:
    """
    Clean up SQL values from the dump.
    Removes surrounding quotes and handles escaped characters.
    """
    value = value.strip()
    if value.upper() == "NULL":
        return None

    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
        # Unescape single quotes
        value = value.replace("\\'", "'")
        return value

    return value


def parse_insert_statement(line: str) -> List[Dict]:
    """
    Parse a MySQL INSERT statement for the users table.
    Returns a list of dictionaries representing user data.
    """
    # Regex to capture the values part of the INSERT statement
    # This is a simplified parser and might need adjustment for complex dumps
    match = re.search(r"INSERT INTO `.*?users` VALUES \((.*)\);", line)
    if not match:
        return []

    values_str = match.group(1)

    # Split by "),(" to separate multiple rows
    # This is a naive split and assumes "),(" doesn't appear inside string literals
    # For a robust solution, a proper SQL parser is better, but this works for standard dumps
    rows = values_str.split("),(")

    users = []
    for row in rows:
        # Clean up leading/trailing parens if they exist (from the split)
        row = row.strip("()")

        # Split fields by comma, respecting quotes
        # Using a regex to split by comma only if not inside quotes
        fields = re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", row)

        # Map fields based on standard WP schema (ID, user_login, user_pass, user_nicename, user_email, user_url, user_registered, user_activation_key, user_status, display_name)
        # Note: The order depends on the dump. Usually it matches the table definition.
        # Based on the user provided schema:
        # ID, user_login, user_pass, user_nicename, user_email, user_url, user_registered, user_activation_key, user_status, display_name

        if len(fields) < 10:
            print(f"Skipping row, not enough fields: {row}")
            continue

        try:
            user_data = {
                "ID": int(parse_sql_value(fields[0])),
                "user_login": parse_sql_value(fields[1]),
                "user_pass": parse_sql_value(fields[2]),
                "user_nicename": parse_sql_value(fields[3]),
                "user_email": parse_sql_value(fields[4]),
                "user_url": parse_sql_value(fields[5]),
                "user_registered": parse_sql_value(fields[6]),
                "user_activation_key": parse_sql_value(fields[7]),
                "user_status": parse_sql_value(fields[8]),
                "display_name": parse_sql_value(fields[9]),
            }
            users.append(user_data)
        except Exception as e:
            print(f"Error parsing row: {row} - {e}")

    return users


async def migrate_users(file_path: str):
    """
    Main migration function.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Starting migration from {file_path}...")

    # Initialize database tables
    await ini_db()

    users_to_create = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "INSERT INTO" in line and "_users`" in line:
                parsed_users = parse_insert_statement(line)
                users_to_create.extend(parsed_users)

    print(f"Found {len(users_to_create)} users in dump.")

    async with AsyncSession(engine) as session:
        count_created = 0
        count_skipped = 0

        for user_data in users_to_create:
            # Check if user exists by email or login
            stmt = select(User).where(
                (User.user_email == user_data["user_email"]) |
                (User.user_login == user_data["user_login"])
            )
            result = await session.exec(stmt)
            existing_user = result.first()

            if existing_user:
                print(f"Skipping existing user: {user_data['user_login']} ({user_data['user_email']})")
                count_skipped += 1
                continue

            # Convert date string to datetime object
            try:
                reg_date = datetime.strptime(user_data["user_registered"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                reg_date = datetime.now()

            new_user = User(
                # We can optionally preserve ID if we want, but auto-increment is usually safer unless relations are critical
                # ID=user_data["ID"],
                user_login=user_data["user_login"],
                user_pass=user_data["user_pass"],
                user_nicename=user_data["user_nicename"],
                user_email=user_data["user_email"],
                user_url=user_data["user_url"] or "",
                user_registered=reg_date,
                user_activation_key=user_data["user_activation_key"],
                user_status=user_data["user_status"],
                display_name=user_data["display_name"]
            )

            session.add(new_user)
            count_created += 1

        await session.commit()
        print(f"Migration complete. Created: {count_created}, Skipped: {count_skipped}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/migrate_wp_users.py <path_to_sql_dump>")
        sys.exit(1)

    dump_file = sys.argv[1]
    asyncio.run(migrate_users(dump_file))
