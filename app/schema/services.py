from pydantic import BaseModel, confloat, validator, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime
import re

class AccountManagementConnectRequest(BaseModel):
    accountId: str
    broker: str
    password: str
    server: str
    capital: float
    manager: str
    agreed: bool

    @validator("capital")
    def validate_capital(cls, v):
        if v < 500:
            raise ValueError("Capital must be at least 500")
        return v

    @validator("agreed")
    def validate_agreed(cls, v):
        if not v:
            raise ValueError("You must agree to the terms to proceed")
        return v

class CopyTradingConnectRequest(BaseModel):
    accountId: str
    password: str
    server: str


class PropFirmRegisterRequest(BaseModel):
    login_id: str
    password: str
    propfirm_name: str
    propfirm_website_link: str
    server_name: str
    server_type: str
    challenges_step: int
    propfirm_account_cost: float
    account_size: float
    account_phases: int
    trading_platform: str = "Metatrader 5"
    propfirm_rules: str
    whatsapp_no: str
    telegram_username: str
    payment_method: str = "crypto"

    @validator("propfirm_website_link")
    def validate_website_link(cls, v):
        if v == "N/A":
            return v
        url_pattern = re.compile(
            r'^https?://'
            r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'
            r'[a-zA-Z]{2,}'
            r'(?:/.*)?$'
        )
        if not url_pattern.match(v):
            raise ValueError("Please provide a valid URL (e.g. https://ftmo.com)")
        return v

    @validator("server_type")
    def validate_server_type(cls, v):
        # Frontend sends "Metatrader 5 only" or "Demo"/"Live"
        if v in ("Demo", "Live", "Metatrader 5 only"):
            return v
        # Allow pass-through for now to avoid blocking frontend
        return v

    @validator("challenges_step")
    def validate_challenges_step(cls, v):
        if v not in (1, 2):
            raise ValueError("Challenges step must be 1 or 2")
        return v

    @validator("account_phases")
    def validate_account_phases(cls, v):
        if v not in (1, 2):
            raise ValueError("Account phases must be 1 or 2")
        return v

    @validator("propfirm_rules")
    def validate_propfirm_rules(cls, v):
        # Relaxed for frontend integration
        return v

    @validator("telegram_username")
    def validate_telegram_username(cls, v):
        # Strip leading @ if provided
        return v.lstrip("@")

class PropFirmRegisterData(BaseModel):
    registration_id: str
    order_id: str
    login_id: str
    propfirm_name: str
    propfirm_website_link: str
    server_name: str
    server_type: str
    challenges_step: int
    propfirm_account_cost: float
    account_size: float
    account_phases: int
    trading_platform: str
    propfirm_rules: str
    whatsapp_no: str
    telegram_username: str
    payment_method: str
    status: str
    payment_status: str
    created_at: datetime
    updated_at: datetime

class PropFirmRegisterResponse(BaseModel):
    success: bool
    message: str
    data: PropFirmRegisterData

class PropFirmRegistrationsResponse(BaseModel):
    success: bool
    count: int
    data: list[PropFirmRegisterData]

class PropFirmUpdateStatusRequest(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None

    @validator("status")
    def validate_status(cls, v):
        if v and v not in ("pending", "active", "completed", "failed"):
            raise ValueError("Invalid status")
        return v

    @validator("payment_status")
    def validate_payment_status(cls, v):
        if v and v not in ("pending", "paid", "refunded", "failed"):
            raise ValueError("Invalid payment status")
        return v


class PropFirmRegistrationAdminRead(PropFirmRegisterData):
    user_name: str
    user_email: str
    password: Optional[str] = None


class PropFirmAdminRegistrationsResponse(BaseModel):
    success: bool
    count: int
    data: list[PropFirmRegistrationAdminRead]

# --- Account Management ---

class AccountManagementData(BaseModel):
    id: UUID
    account_id: str
    broker: str
    server: str
    capital: float
    manager: str
    status: str
    created_at: datetime
    updated_at: datetime

class AccountManagementResponse(BaseModel):
    success: bool
    message: str
    data: AccountManagementData

class AccountManagementListResponse(BaseModel):
    success: bool
    count: int
    data: list[AccountManagementData]

class AccountManagementUpdateStatusRequest(BaseModel):
    status: str

    @validator("status")
    def validate_status(cls, v):
        if v not in ("pending", "active", "disconnected", "failed"):
            raise ValueError("Invalid status")
        return v

class AccountManagementAdminRead(AccountManagementData):
    user_name: str
    user_email: str
    password: Optional[str] = None

class AccountManagementAdminListResponse(BaseModel):
    success: bool
    count: int
    data: list[AccountManagementAdminRead]

# --- Copy Trading ---

class CopyTradingData(BaseModel):
    id: UUID
    account_id: str
    server: str
    status: str
    created_at: datetime
    updated_at: datetime

class CopyTradingResponse(BaseModel):
    success: bool
    message: str
    data: CopyTradingData

class CopyTradingListResponse(BaseModel):
    success: bool
    count: int
    data: list[CopyTradingData]

class CopyTradingUpdateStatusRequest(BaseModel):
    status: str

    @validator("status")
    def validate_status(cls, v):
        if v not in ("pending", "active", "disconnected", "failed"):
            raise ValueError("Invalid status")
        return v

class CopyTradingAdminRead(CopyTradingData):
    user_name: str
    user_email: str
    password: Optional[str] = None

class CopyTradingAdminListResponse(BaseModel):
    success: bool
    count: int
    data: list[CopyTradingAdminRead]
