"""
WordPress-compatible password hashing utilities.

Supports:
1. phpass (Portable PHP password hashing) - Used in WordPress < 6.8
2. bcrypt - Used in WordPress 6.8+ via PHP's password_hash()

This allows imported WordPress users to authenticate with their existing passwords.
"""
from passlib.hash import phpass, bcrypt as passlib_bcrypt
import hashlib
import base64
import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from jose import jwt, JWTError

from app.core.config import settings


def verify_bcrypt_password(password: str, stored_hash: str) -> bool:
    """
    Verify a password against a bcrypt hash.

    WordPress 6.8+ uses bcrypt via PHP's password_hash().
    PHP bcrypt hashes start with $2y$ (compatible with Python's $2b$).

    Args:
        password: Plain text password to verify
        stored_hash: Bcrypt hash (starts with $2y$, $2b$, $2a$)

    Returns:
        True if password matches, False otherwise
    """
    try:
        # Normalize stored hash from DB (strip accidental whitespace)
        hash_to_check = (stored_hash or "").strip()

        # Some WordPress installations (or plugins) store bcrypt hashes with a
        # leading "$wp$" prefix, e.g. "$wp$2y$...". Strip that if present.
        if hash_to_check.startswith("$wp$"):
            # Remove "$wp$" to get valid bcrypt hash
            # e.g. "$wp$2y$..." -> "$2y$..."
            hash_to_check = "$" + hash_to_check[4:]

        # Handle unusual "$2b$2y$" prefix by stripping the redundant "$2b"
        if hash_to_check.startswith("$2b$2y$"):
            hash_to_check = "$" + hash_to_check[4:]

        # passlib.hash.bcrypt handles $2a, $2b, $2y automatically.
        # It also handles the compatibility between PHP and Python bcrypt.
        return passlib_bcrypt.verify(password, hash_to_check)
    except Exception:
        return False


def hash_password(password: str) -> str:
    """
    Hash a password using WordPress-style phpass.

    This ensures 100% compatibility with WordPress.
    The hash will start with $P$...

    Args:
        password: Plain text password to hash

    Returns:
        phpass hash string
    """
    return phpass.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify a password against either phpass or bcrypt hash.

    This function supports both WordPress legacy phpass hashes
    and modern bcrypt hashes, allowing seamless authentication
    for imported WordPress users.

    Args:
        password: Plain text password to verify
        stored_hash: Hash from database (phpass or bcrypt)

    Returns:
        True if password matches, False otherwise
    """
    stored_hash = (stored_hash or "").strip()
    if not stored_hash:
        return False

    # Check if it's a phpass hash (WordPress default)
    if (stored_hash.startswith("$P$") or
        stored_hash.startswith("$H$") or
        stored_hash.startswith("$2") or
        stored_hash.startswith("$wp$")):

        # Try phpass first (most common for WP)
        if stored_hash.startswith("$P$") or stored_hash.startswith("$H$"):
            try:
                return phpass.verify(password, stored_hash)
            except ValueError:
                return False

        # Try bcrypt (including legacy prefixes handled by verify_bcrypt_password)
        return verify_bcrypt_password(password, stored_hash)

    # Legacy MD5 hash (very old WordPress, not recommended)
    if len(stored_hash) == 32 and all(c in "0123456789abcdef" for c in stored_hash.lower()):
        return hashlib.md5(password.encode("utf-8")).hexdigest().lower() == stored_hash.lower()

    return False


def generate_verification_code() -> str:
    """Generate a 6-digit verification code for email verification."""
    return "".join(secrets.choice(string.digits) for _ in range(6))


def generate_reset_token() -> str:
    """Generate a secure random token for password reset."""
    return secrets.token_urlsafe(32)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Payload data to encode
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})

    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token.

    Args:
        data: Payload data to encode

    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})

    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
