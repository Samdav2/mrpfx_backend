import subprocess
import sys

# === List of required packages for the project ===
packages = [
    # Core Framework
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "gunicorn>=21.2.0",

    # Database & ORM
    "sqlmodel>=0.0.14",
    "sqlalchemy[asyncio]>=2.0.25",
    "asyncpg>=0.29.0",       # PostgreSQL
    "aiosqlite>=0.20.0",     # SQLite
    "PyMySQL>=1.1.0",
    "alembic>=1.13.0",

    # Authentication & Security
    "python-jose[cryptography]>=3.3.0",
    "bcrypt>=4.1.2",
    "passlib>=1.7.4",
    "python-multipart>=0.0.6",

    # Settings & Validation
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "python-dotenv>=1.0.0",
    "email-validator>=2.1.0",

    # Development & Utils
    "httpx>=0.26.0",
    "Pillow>=11.1.0",
    "phpserialize>=1.3",
    "jinja2>=3.1.0",
    "aiosmtplib>=3.0.0",
    "redis>=5.0.0",
    "slowapi>=0.1.9",
    "orjson>=3.9.0",
    "networkx>=3.0"
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
