import subprocess
import sys

# === List of required packages for the project ===
packages = [
    # Core Framework
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",

    # Database & ORM
    "sqlalchemy>=2.0.0",
    "sqlmodel>=0.0.14",
    "aiosqlite>=0.19.0",     # SQLite async support
    "asyncpg>=0.29.0",       # PostgreSQL async support
    "alembic>=1.13.0",
    "PyMySQL>=1.1.0",        # Future MySQL connection support

    # Validation & Settings
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "email-validator>=2.0.0",

    # Authentication & Security
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "bcrypt>=4.0.0",
    "python-multipart>=0.0.6",

    # Game Engine & Logic
    "networkx>=3.0",

    # Caching & HTTP
    "redis>=5.0.0",
    "httpx>=0.26.0",

    # Rate Limiting
    "slowapi>=0.1.9",

    # Production Server & Performance
    "gunicorn>=21.0.0",
    "orjson>=3.9.0",

    # Email
    "aiosmtplib>=3.0.0",
    "jinja2>=3.1.0"
]

def install(package):
    """Install a Python package using pip."""
    try:
        print(f"📦 Installing {package} ...")
        # Use sys.executable to ensure pip is from the correct virtual env
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}\n")

if __name__ == "__main__":
    print("--- Starting project dependency installation ---")
    print(f"Using Python: {sys.executable}")
    for pkg in packages:
        install(pkg)
    print("--- All packages processed ---")
