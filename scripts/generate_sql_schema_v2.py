import sys
import os
import importlib
import pkgutil

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import mysql

# Explicitly import all packages in app.model
import app.model.user
import app.model.services
import app.model.traders
import app.model.crypto_payment

# Dynamically import all modules in app.model.wordpress
import app.model.wordpress as wp_pkg
path = os.path.dirname(wp_pkg.__file__)
for loader, module_name, is_pkg in pkgutil.walk_packages([path], wp_pkg.__name__ + "."):
    try:
        importlib.import_module(module_name)
    except Exception as e:
        print(f"-- Warning: Could not import {module_name}: {e}", file=sys.stderr)

print(f"-- Total tables registered: {len(SQLModel.metadata.tables)}", file=sys.stderr)

def generate_sql():
    print("-- MRPFX Complete Database Schema (MySQL)")
    print("SET FOREIGN_KEY_CHECKS = 0;\n")

    dialect = mysql.dialect()

    # We use sorted_tables to ensure parent tables come before child tables if possible
    # though with FOREIGN_KEY_CHECKS = 0 it's less critical.
    for table in SQLModel.metadata.sorted_tables:
        print(f"-- Table Name: {table.name}")
        create_stmt = CreateTable(table).compile(dialect=dialect)
        sql = str(create_stmt).replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
        print(f"{sql};")
        print()

    print("\nSET FOREIGN_KEY_CHECKS = 1;")

if __name__ == "__main__":
    generate_sql()
