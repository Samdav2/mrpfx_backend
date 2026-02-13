"""
WordPress-compatible password hashing utilities.

Supports:
1. phpass (Portable PHP password hashing) - Used in WordPress < 6.8
2. bcrypt - Used in WordPress 6.8+ via PHP's password_hash()

This allows imported WordPress users to authenticate with their existing passwords.
"""
import hashlib
import base64
import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from jose import jwt, JWTError
import bcrypt

from app.core.config import settings


# phpass itoa64 alphabet used for encoding
ITOA64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def _encode64(input_bytes: bytes, count: int) -> str:
    """
    Encode bytes to phpass base64 format.
    This is the custom base64 encoding used by phpass.
    """
    output = ""
    i = 0
    while i < count:
        value = input_bytes[i]
        i += 1
        output += ITOA64[value & 0x3f]

        if i < count:
            value |= input_bytes[i] << 8
        output += ITOA64[(value >> 6) & 0x3f]

        if i >= count:
            break
        i += 1

        if i < count:
            value |= input_bytes[i] << 16
        output += ITOA64[(value >> 12) & 0x3f]

        if i >= count:
            break
        i += 1
        output += ITOA64[(value >> 18) & 0x3f]

    return output


def _crypt_private(password: str, stored_hash: str) -> str:
    """
    Compute phpass portable hash for password verification.

    Args:
        password: Plain text password
        stored_hash: The stored hash from WordPress database

    Returns:
        Computed hash to compare with stored_hash
    """
    output = "*0"
    if stored_hash.startswith(output):
        output = "*1"

    # Check for valid phpass hash format
    if not stored_hash.startswith("$P$") and not stored_hash.startswith("$H$"):
        return output

    # Extract iteration count (log2)
    count_log2_char = stored_hash[3]
    count_log2 = ITOA64.find(count_log2_char)

    if count_log2 < 7 or count_log2 > 30:
        return output

    count = 1 << count_log2

    # Extract salt (8 characters after the identifier)
    salt = stored_hash[4:12]
    if len(salt) != 8:
        return output

    # Compute hash
    hash_value = hashlib.md5((salt + password).encode("utf-8")).digest()

    for _ in range(count):
        hash_value = hashlib.md5(hash_value + password.encode("utf-8")).digest()

    output = stored_hash[:12]  # $P$B + salt
    output += _encode64(hash_value, 16)

    return output


def verify_phpass_password(password: str, stored_hash: str) -> bool:
    """
    Verify a password against a WordPress phpass hash.

    Args:
        password: Plain text password to verify
        stored_hash: WordPress phpass hash (starts with $P$ or $H$)

    Returns:
        True if password matches, False otherwise
    """
    if not stored_hash.startswith("$P$") and not stored_hash.startswith("$H$"):
        return False

    computed_hash = _crypt_private(password, stored_hash)
    return computed_hash == stored_hash


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
        # PHP uses $2y$ but Python bcrypt uses $2b$
        # They are compatible, but we need to handle the prefix
        hash_to_check = stored_hash
        if hash_to_check.startswith("$2y$"):
            hash_to_check = "$2b$" + hash_to_check[4:]

        return bcrypt.checkpw(
            password.encode("utf-8"),
            hash_to_check.encode("utf-8")
        )
    except Exception:
        return False


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt (WordPress 6.8+ compatible).

    New passwords are always hashed with bcrypt for security.
    The hash uses $2b$ prefix which is compatible with PHP's $2y$.

    Args:
        password: Plain text password to hash

    Returns:
        Bcrypt hash string
    """
    salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


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
    if not stored_hash:
        return False

    # Check if it's a phpass hash (WordPress < 6.8)
    if stored_hash.startswith("$P$") or stored_hash.startswith("$H$"):
        return verify_phpass_password(password, stored_hash)

    # Check if it's a bcrypt hash (WordPress 6.8+ or new users)
    if stored_hash.startswith("$2"):
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
