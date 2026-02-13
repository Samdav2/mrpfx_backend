"""
User management plugin database models.
Includes WP User Manager and Ultimate Member.
Maps to tables with prefixes 8jH_wpum_*, 8jH_um_*
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field


# =============================================================================
# WP User Manager Models
# =============================================================================

class WPUMFieldsGroup(SQLModel, table=True):
    """WPUM field groups (8jH_wpum_fieldsgroups)"""
    __tablename__ = "8jH_wpum_fieldsgroups"

    id: Optional[int] = Field(default=None, primary_key=True)
    group_order: int = Field(default=0)
    is_primary: int = Field(default=0)
    name: str = Field(max_length=190, default="")
    description: Optional[str] = Field(default=None)


class WPUMField(SQLModel, table=True):
    """WPUM fields (8jH_wpum_fields)"""
    __tablename__ = "8jH_wpum_fields"

    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(default=0, foreign_key="8jH_wpum_fieldsgroups.id")
    field_order: int = Field(default=0)
    type: str = Field(max_length=20, default="text")
    name: str = Field(max_length=255, default="")
    description: Optional[str] = Field(default=None)


class WPUMFieldMeta(SQLModel, table=True):
    """WPUM field meta (8jH_wpum_fieldmeta)"""
    __tablename__ = "8jH_wpum_fieldmeta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    wpum_field_id: int = Field(default=0, foreign_key="8jH_wpum_fields.id")
    meta_key: Optional[str] = Field(default=None, max_length=255)
    meta_value: Optional[str] = Field(default=None)


class WPUMRegistrationForm(SQLModel, table=True):
    """WPUM registration forms (8jH_wpum_registration_forms)"""
    __tablename__ = "8jH_wpum_registration_forms"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, default="")


class WPUMRegistrationFormMeta(SQLModel, table=True):
    """WPUM registration form meta (8jH_wpum_registration_formmeta)"""
    __tablename__ = "8jH_wpum_registration_formmeta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    wpum_registration_form_id: int = Field(default=0, foreign_key="8jH_wpum_registration_forms.id")
    meta_key: Optional[str] = Field(default=None, max_length=255)
    meta_value: Optional[str] = Field(default=None)


class WPUMSearchField(SQLModel, table=True):
    """WPUM search fields (8jH_wpum_search_fields)"""
    __tablename__ = "8jH_wpum_search_fields"

    id: Optional[int] = Field(default=None, primary_key=True)
    meta_key: str = Field(max_length=255, default="")


class WPUMStripeSubscription(SQLModel, table=True):
    """WPUM Stripe subscriptions (8jH_wpum_stripe_subscriptions)"""
    __tablename__ = "8jH_wpum_stripe_subscriptions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=0, foreign_key="8jH_users.ID")
    customer_id: str = Field(max_length=255, default="")
    plan_id: str = Field(max_length=255, default="")
    subscription_id: str = Field(max_length=255, default="")
    trial_ends_at: Optional[datetime] = Field(default=None)
    ends_at: Optional[datetime] = Field(default=None)
    gateway_mode: str = Field(max_length=4, default="")
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)


class WPUMStripeInvoice(SQLModel, table=True):
    """WPUM Stripe invoices (8jH_wpum_stripe_invoices)"""
    __tablename__ = "8jH_wpum_stripe_invoices"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=0, foreign_key="8jH_users.ID")
    invoice_id: str = Field(max_length=255, default="")
    total: Decimal = Field(default=0)
    currency: str = Field(max_length=20, default="")
    gateway_mode: str = Field(max_length=4, default="")
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)


# =============================================================================
# Ultimate Member Models
# =============================================================================

class UMMetadata(SQLModel, table=True):
    """Ultimate Member metadata (8jH_um_metadata)"""
    __tablename__ = "8jH_um_metadata"

    umeta_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=0, foreign_key="8jH_users.ID")
    um_key: Optional[str] = Field(default=None, max_length=255)
    um_value: Optional[str] = Field(default=None)
