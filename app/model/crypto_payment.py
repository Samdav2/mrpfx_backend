from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, Dict, Any

class CryptoPayment(SQLModel, table=True):
    """Database model for crypto payments."""
    __tablename__ = "8jH_cryptopayments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: int = Field(foreign_key="8jH_users.ID", index=True)

    payment_id: Optional[str] = Field(default=None, index=True)
    invoice_id: Optional[str] = Field(default=None, index=True)
    order_id: Optional[str] = Field(default=None, index=True)
    order_description: Optional[str] = Field(default=None)

    price_amount: float
    price_currency: str = Field(default="usd")

    pay_amount: Optional[float] = Field(default=None)
    pay_currency: Optional[str] = Field(default=None)
    pay_address: Optional[str] = Field(default=None)
    payin_extra_id: Optional[str] = Field(default=None)

    payment_status: str = Field(default="waiting", index=True)
    actually_paid: Optional[float] = Field(default=None)
    purchase_id: Optional[str] = Field(default=None)

    outcome_amount: Optional[float] = Field(default=None)
    outcome_currency: Optional[str] = Field(default=None)

    ipn_callback_url: Optional[str] = Field(default=None)
    invoice_url: Optional[str] = Field(default=None)

    is_fixed_rate: bool = Field(default=False)
    is_fee_paid_by_user: bool = Field(default=False)

    # Store any extra data from IPN or API in a JSON field if needed
    extra_data: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
