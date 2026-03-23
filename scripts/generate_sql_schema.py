import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import mysql

# Import ALL models
print("-- Importing models...", file=sys.stderr)
try:
    from app.model.crypto_payment import CryptoPayment
    from app.model.services import AccountManagementConnection, CopyTradingConnection, PropFirmRegistration
    from app.model.traders import Trader, TraderPerformance
    from app.model.user import User
    import app.model.wordpress
    print(f"-- {len(SQLModel.metadata.tables)} tables found.", file=sys.stderr)
except Exception as e:
    print(f"-- Error importing models: {e}", file=sys.stderr)
    sys.exit(1)

def generate_sql():
    print("-- MRPFX Database Schema Export (MySQL)")
    print("SET FOREIGN_KEY_CHECKS = 0;\n")

    dialect = mysql.dialect()

    # Sort tables to handle dependencies if any (though create_all handles this)
    for table in SQLModel.metadata.sorted_tables:
        print(f"-- Table: {table.name}")
        # Generate the CREATE TABLE statement using MySQL dialect
        create_stmt = CreateTable(table).compile(dialect=dialect)
        # Add IF NOT EXISTS and convert to string
        sql = str(create_stmt).replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
        print(f"{sql};")
        print()

    print("\nSET FOREIGN_KEY_CHECKS = 1;")

if __name__ == "__main__":
    generate_sql()
