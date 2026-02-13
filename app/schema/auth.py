from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class SignupRequest(BaseModel):
    """Request schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    username: str = Field(..., min_length=3, max_length=60)
    display_name: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!",
                "username": "johndoe",
                "display_name": "John Doe"
            }
        }


class LoginRequest(BaseModel):
    """Request schema for user login. Can use email or username."""
    login: str = Field(..., description="Email or username")
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "login": "user@example.com",
                "password": "SecurePass123!"
            }
        }


class TokenResponse(BaseModel):
    """Response schema for authentication tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Access token expiration in seconds")


class VerifyEmailRequest(BaseModel):
    """Request schema for email verification."""
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "code": "123456"
            }
        }


class ResendVerificationRequest(BaseModel):
    """Request schema to resend verification email."""
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    """Request schema for forgot password."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Request schema for password reset."""
    email: EmailStr
    token: str
    new_password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "token": "reset-token-here",
                "new_password": "NewSecurePass123!"
            }
        }


class RefreshTokenRequest(BaseModel):
    """Request schema for token refresh."""
    refresh_token: str


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    success: bool = True
