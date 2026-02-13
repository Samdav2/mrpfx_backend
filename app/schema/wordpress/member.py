from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel

class SWPMMemberBase(BaseModel):
    user_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    membership_level: int
    account_state: Optional[str] = "pending"
    company_name: Optional[str] = None

class SWPMMemberCreate(SWPMMemberBase):
    password: str

class SWPMMemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    membership_level: Optional[int] = None
    account_state: Optional[str] = None
    password: Optional[str] = None

class SWPMMemberRead(SWPMMemberBase):
    member_id: int
    member_since: date
    last_accessed: datetime

    class Config:
        from_attributes = True
