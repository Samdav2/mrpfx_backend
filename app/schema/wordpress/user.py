from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class WPUserBase(BaseModel):
    user_login: str
    user_nicename: Optional[str] = None
    user_email: str
    user_url: Optional[str] = None
    display_name: Optional[str] = None
    user_status: int = 0

class WPUserCreate(WPUserBase):
    user_pass: str

class WPUserUpdate(BaseModel):
    user_nicename: Optional[str] = None
    user_email: Optional[str] = None
    user_url: Optional[str] = None
    display_name: Optional[str] = None
    user_status: Optional[int] = None
    user_pass: Optional[str] = None

class WPUserRead(WPUserBase):
    ID: int
    user_registered: datetime

    class Config:
        from_attributes = True
