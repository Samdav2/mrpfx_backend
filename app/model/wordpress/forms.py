"""
Form plugin database models.
Includes WPForms.
Maps to tables with prefix 8jH_wpforms_*
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field


class WPFormsLog(SQLModel, table=True):
    """WPForms logs (8jH_wpforms_logs)"""
    __tablename__ = "8jH_wpforms_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, default="")
    message: str = Field(default="")
    types: str = Field(max_length=255, default="")
    create_at: datetime = Field(default_factory=datetime.now)
    form_id: Optional[int] = Field(default=None)
    entry_id: Optional[int] = Field(default=None)
    user_id: Optional[int] = Field(default=None)


class WPFormsPayment(SQLModel, table=True):
    """WPForms payments (8jH_wpforms_payments)"""
    __tablename__ = "8jH_wpforms_payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    form_id: int = Field(default=0)
    status: str = Field(max_length=10, default="")
    subtotal_amount: Decimal = Field(default=0)
    discount_amount: Decimal = Field(default=0)
    total_amount: Decimal = Field(default=0)
    currency: str = Field(max_length=3, default="")
    entry_id: int = Field(default=0)
    gateway: str = Field(max_length=20, default="")
    type: str = Field(max_length=12, default="")
    mode: str = Field(max_length=4, default="")
    transaction_id: str = Field(max_length=40, default="")
    customer_id: str = Field(max_length=40, default="")
    subscription_id: str = Field(max_length=40, default="")
    subscription_status: str = Field(max_length=10, default="")
    title: str = Field(max_length=255, default="")
    date_created_gmt: datetime = Field(default_factory=datetime.now)
    date_updated_gmt: datetime = Field(default_factory=datetime.now)
    is_published: int = Field(default=1)


class WPFormsPaymentMeta(SQLModel, table=True):
    """WPForms payment meta (8jH_wpforms_payment_meta)"""
    __tablename__ = "8jH_wpforms_payment_meta"

    id: Optional[int] = Field(default=None, primary_key=True)
    payment_id: int = Field(default=0, foreign_key="8jH_wpforms_payments.id")
    meta_key: Optional[str] = Field(default=None, max_length=255)
    meta_value: Optional[str] = Field(default=None)


class WPFormsTaskMeta(SQLModel, table=True):
    """WPForms task meta (8jH_wpforms_tasks_meta)"""
    __tablename__ = "8jH_wpforms_tasks_meta"

    id: Optional[int] = Field(default=None, primary_key=True)
    action: str = Field(max_length=255, default="")
    data: str = Field(default="")
    date: datetime = Field(default_factory=datetime.now)
