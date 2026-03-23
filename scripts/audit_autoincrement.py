import sys
import os
import importlib
import pkgutil

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel

# Import all modules to populate metadata
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

print("--- Auditing Tables for Multiple Autoincrement ---")
found_issues = False
for table_name, table in SQLModel.metadata.tables.items():
    auto_cols = [c.name for c in table.columns if c.autoincrement is True]
    if len(auto_cols) > 1:
        print(f"Table '{table_name}' has {len(auto_cols)} autoincrement columns: {', '.join(auto_cols)}")
        found_issues = True

if not found_issues:
    print("No issues found in metadata!")
else:
    print("\nPlease fix these tables by removing 'autoincrement=True' from composite keys.")
