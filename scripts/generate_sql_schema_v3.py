import sys
import os
import importlib
import pkgutil

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel
from sqlalchemy.schema import CreateTable, CreateIndex
from sqlalchemy.dialects import mysql

# Import models
import app.model.user
import app.model.services
import app.model.traders
import app.model.crypto_payment
import app.model.wordpress as wp_pkg
path = os.path.dirname(wp_pkg.__file__)
for loader, module_name, is_pkg in pkgutil.walk_packages([path], wp_pkg.__name__ + "."):
    try:
        importlib.import_module(module_name)
    except:
        pass

def generate_sql():
    print("-- MRPFX Final Complete Database Schema (MySQL)")
    print("SET FOREIGN_KEY_CHECKS = 0;\n")

    dialect = mysql.dialect()

    for table in SQLModel.metadata.sorted_tables:
        print(f"-- Table Name: {table.name}")

        # Get the CREATE TABLE statement
        create_stmt = CreateTable(table).compile(dialect=dialect)
        sql = str(create_stmt).strip()

        # Ensure IF NOT EXISTS
        if "CREATE TABLE" in sql and "IF NOT EXISTS" not in sql:
            sql = sql.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")

        print(f"{sql};")

        # Also generate indexes if they are not in the CREATE TABLE
        for index in table.indexes:
            # We skip indexes that are likely already handled or unnamed
            idx_stmt = CreateIndex(index).compile(dialect=dialect)
            print(f"{idx_stmt};")

        print()

    print("\nSET FOREIGN_KEY_CHECKS = 1;")

if __name__ == "__main__":
    generate_sql()
