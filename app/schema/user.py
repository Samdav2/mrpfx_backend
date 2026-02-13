from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Internal schema for creating a user."""
    user_login: str
    user_pass: str
    user_email: str
    user_nicename: str
    user_url: str = ""
    user_activation_key: Optional[str] = None
    user_status: int = 0  # 0 = unverified, 1 = active
    display_name: Optional[str] = None


class UserResponse(BaseModel):
    """Public user data response."""
    ID: int
    user_login: str
    user_nicename: str
    user_email: EmailStr
    user_url: str
    user_registered: datetime
    user_status: int = 0
    display_name: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    display_name: Optional[str] = None
    user_url: Optional[str] = None
    user_nicename: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    """Request schema for changing password."""
    current_password: str
    new_password: str = Field(..., min_length=8)
