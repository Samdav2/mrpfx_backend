"""
Simple WordPress Membership Plugin (SWPM) database models.
Maps to tables with prefix 8jH_swpm_*

This is the main membership plugin used for user subscriptions.
"""
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class SWPMMember(SQLModel, table=True):
    """SWPM members table (8jH_swpm_members_tbl)"""
    __tablename__ = "8jH_swpm_members_tbl"

    member_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = Field(max_length=255, default="")
    first_name: Optional[str] = Field(default="", max_length=64)
    last_name: Optional[str] = Field(default="", max_length=64)
    password: str = Field(max_length=255, default="")
    member_since: date = Field(default_factory=date.today)
    membership_level: int = Field(default=0)
    more_membership_levels: Optional[str] = Field(default=None, max_length=100)
    account_state: Optional[str] = Field(default="pending", max_length=20)  # active, inactive, activation_required, expired, pending, unsubscribed
    last_accessed: datetime = Field(default_factory=datetime.now)
    last_accessed_from_ip: str = Field(max_length=128, default="")
    email: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=64)
    address_street: Optional[str] = Field(default=None, max_length=255)
    address_city: Optional[str] = Field(default=None, max_length=255)
    address_state: Optional[str] = Field(default=None, max_length=255)
    address_zipcode: Optional[str] = Field(default=None, max_length=255)
    home_page: Optional[str] = Field(default=None, max_length=255)
    country: Optional[str] = Field(default=None, max_length=255)
    gender: Optional[str] = Field(default="not specified", max_length=15)  # male, female, not specified
    referrer: Optional[str] = Field(default=None, max_length=255)
    extra_info: Optional[str] = Field(default=None)
    reg_code: Optional[str] = Field(default=None, max_length=255)
    subscription_starts: Optional[date] = Field(default=None)
    initial_membership_level: Optional[int] = Field(default=None)
    txn_id: Optional[str] = Field(default="", max_length=255)
    subscr_id: Optional[str] = Field(default="", max_length=255)
    company_name: Optional[str] = Field(default="", max_length=255)
    notes: Optional[str] = Field(default=None)
    flags: Optional[int] = Field(default=0)
    profile_image: Optional[str] = Field(default="", max_length=255)


class SWPMMembership(SQLModel, table=True):
    """SWPM membership levels table (8jH_swpm_membership_tbl)"""
    __tablename__ = "8jH_swpm_membership_tbl"

    id: Optional[int] = Field(default=None, primary_key=True)
    alias: str = Field(max_length=127, default="")
    role: str = Field(max_length=255, default="subscriber")
    permissions: int = Field(default=0)
    subscription_period: str = Field(max_length=11, default="-1")
    subscription_duration_type: int = Field(default=0)
    subscription_unit: Optional[str] = Field(default=None, max_length=20)
    loginredirect_page: Optional[str] = Field(default=None)
    category_list: Optional[str] = Field(default=None)
    page_list: Optional[str] = Field(default=None)
    post_list: Optional[str] = Field(default=None)
    comment_list: Optional[str] = Field(default=None)
    attachment_list: Optional[str] = Field(default=None)
    custom_post_list: Optional[str] = Field(default=None)
    disable_bookmark_list: Optional[str] = Field(default=None)
    options: Optional[str] = Field(default=None)
    protect_older_posts: bool = Field(default=False)
    campaign_name: str = Field(max_length=255, default="")


class SWPMMembershipMeta(SQLModel, table=True):
    """SWPM membership meta table (8jH_swpm_membership_meta_tbl)"""
    __tablename__ = "8jH_swpm_membership_meta_tbl"

    id: Optional[int] = Field(default=None, primary_key=True)
    level_id: int = Field(foreign_key="8jH_swpm_membership_tbl.id")
    meta_key: str = Field(max_length=255, default="")
    meta_label: Optional[str] = Field(default=None, max_length=255)
    meta_value: Optional[str] = Field(default=None)
    meta_type: str = Field(max_length=255, default="text")
    meta_default: Optional[str] = Field(default=None)
    meta_context: str = Field(max_length=255, default="default")


class SWPMPayment(SQLModel, table=True):
    """SWPM payments table (8jH_swpm_payments_tbl)"""
    __tablename__ = "8jH_swpm_payments_tbl"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: Optional[str] = Field(default=None, max_length=255)
    first_name: Optional[str] = Field(default="", max_length=64)
    last_name: Optional[str] = Field(default="", max_length=64)
    member_id: Optional[str] = Field(default="", max_length=16)
    membership_level: Optional[str] = Field(default="", max_length=64)
    txn_date: date = Field(default_factory=date.today)
    txn_id: str = Field(max_length=255, default="")
    subscr_id: str = Field(max_length=255, default="")
    reference: str = Field(max_length=255, default="")
    payment_amount: str = Field(max_length=32, default="")
    gateway: Optional[str] = Field(default="", max_length=32)
    status: Optional[str] = Field(default="", max_length=255)
    ip_address: Optional[str] = Field(default="", max_length=128)
