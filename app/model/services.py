from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional
from sqlalchemy.dialects.mysql import BIGINT

class AccountManagementConnection(SQLModel, table=True):
    """Database model for MT5 Account Management Connections."""
    __tablename__ = "8jH_account_management_connections"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="8jH_users.ID", index=True, sa_type=BIGINT(unsigned=True))

    account_id: str
    password: str # Encrypted!
    server: str
    broker: str # Added broker field
    capital: float
    manager: str
    agreed: bool = Field(default=True)

    status: str = Field(default="pending", index=True) # pending, active, disconnected, failed

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CopyTradingConnection(SQLModel, table=True):
    """Database model for MT5 Copy Trading Connections."""
    __tablename__ = "8jH_copy_trading_connections"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="8jH_users.ID", index=True, sa_type=BIGINT(unsigned=True))

    account_id: str
    password: str # Encrypted!
    server: str

    status: str = Field(default="pending", index=True) # pending, active, disconnected, failed

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PropFirmRegistration(SQLModel, table=True):
    """Database model for Prop Firm (Pass Funded Accounts) registrations."""
    __tablename__ = "8jH_prop_firm_registrations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="8jH_users.ID", index=True, sa_type=BIGINT(unsigned=True))

    login_id: str
    password: str  # Fernet-encrypted before storage
    propfirm_name: str
    propfirm_website_link: str
    server_name: str
    server_type: str  # Demo or Live
    challenges_step: int
    propfirm_account_cost: float
    account_size: float
    account_phases: int
    trading_platform: str = Field(default="Metatrader 5")
    propfirm_rules: str
    whatsapp_no: str
    telegram_username: str

    status: str = Field(default="pending", index=True)  # pending, active, completed, failed
    payment_status: str = Field(default="pending", index=True)
    payment_method: str = Field(default="crypto", index=True)  # card, crypto
    order_id: Optional[str] = Field(default=None, index=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
