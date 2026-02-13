"""
Miscellaneous WordPress plugin database models.
Includes Jetpack, WP Mail SMTP, WP-Optimize, Task Manager, WP Webhooks Pro,
X Currency, Skrill, WooCommerce Subscriptions, WC Admin Notes, and more.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field


# =============================================================================
# Jetpack Models
# =============================================================================

class JetpackSyncQueue(SQLModel, table=True):
    """Jetpack sync queue (8jH_jetpack_sync_queue)"""
    __tablename__ = "8jH_jetpack_sync_queue"

    ID: Optional[int] = Field(default=None, primary_key=True)
    queue_id: str = Field(max_length=50, default="")
    event_id: str = Field(max_length=100, default="")
    event_payload: str = Field(default="")
    timestamp: Optional[datetime] = Field(default=None)


# =============================================================================
# WP Mail SMTP Models
# =============================================================================

class WPMailSMTPDebugEvent(SQLModel, table=True):
    """WP Mail SMTP debug events (8jH_wpmailsmtp_debug_events)"""
    __tablename__ = "8jH_wpmailsmtp_debug_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    content: Optional[str] = Field(default=None)
    initiator: Optional[str] = Field(default=None)
    event_type: int = Field(default=0)
    created_at: Optional[datetime] = Field(default=None)


class WPMailSMTPTaskMeta(SQLModel, table=True):
    """WP Mail SMTP task meta (8jH_wpmailsmtp_tasks_meta)"""
    __tablename__ = "8jH_wpmailsmtp_tasks_meta"

    id: Optional[int] = Field(default=None, primary_key=True)
    action: str = Field(max_length=255, default="")
    data: str = Field(default="")
    date: datetime = Field(default_factory=datetime.now)


class WPMailLog(SQLModel, table=True):
    """WP Mail Logging (8jH_wpml_mails)"""
    __tablename__ = "8jH_wpml_mails"

    mail_id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: Optional[datetime] = Field(default=None)
    host: str = Field(max_length=200, default="0")
    receiver: str = Field(max_length=200, default="0")
    subject: str = Field(max_length=200, default="0")
    message: Optional[str] = Field(default=None)
    headers: Optional[str] = Field(default=None)
    attachments: str = Field(max_length=800, default="0")
    error: Optional[str] = Field(default="", max_length=400)
    plugin_version: str = Field(max_length=200, default="0")


# =============================================================================
# WP-Optimize Models
# =============================================================================

class WPO404Detector(SQLModel, table=True):
    """WP-Optimize 404 detector (8jH_wpo_404_detector)"""
    __tablename__ = "8jH_wpo_404_detector"

    ID: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(default="")
    request_timestamp: int = Field(default=0)
    request_count: int = Field(default=0)
    referrer: str = Field(default="")


# =============================================================================
# Task Manager Models
# =============================================================================

class TMTask(SQLModel, table=True):
    """Task Manager tasks (8jH_tm_tasks)"""
    __tablename__ = "8jH_tm_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=0, foreign_key="8jH_users.ID")
    type: str = Field(max_length=300, default="")
    class_identifier: Optional[str] = Field(default="0", max_length=300)
    attempts: Optional[int] = Field(default=0)
    description: Optional[str] = Field(default=None, max_length=300)
    time_created: Optional[datetime] = Field(default=None)
    last_locked_at: Optional[int] = Field(default=0)
    status: Optional[str] = Field(default=None, max_length=300)


class TMTaskMeta(SQLModel, table=True):
    """Task Manager task meta (8jH_tm_taskmeta)"""
    __tablename__ = "8jH_tm_taskmeta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(default=0, foreign_key="8jH_tm_tasks.id")
    meta_key: Optional[str] = Field(default=None, max_length=255)
    meta_value: Optional[str] = Field(default=None)


# =============================================================================
# WP Webhooks Pro Models
# =============================================================================

class WPWebhooksAuth(SQLModel, table=True):
    """WP Webhooks Pro authentication (8jH_wpwhpro_authentication)"""
    __tablename__ = "8jH_wpwhpro_authentication"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None, max_length=100)
    auth_type: Optional[str] = Field(default=None, max_length=100)
    template: Optional[str] = Field(default=None)
    log_time: Optional[datetime] = Field(default=None)


# =============================================================================
# X Currency Models
# =============================================================================

class XCurrency(SQLModel, table=True):
    """X Currency settings (8jH_x_currency)"""
    __tablename__ = "8jH_x_currency"

    id: Optional[int] = Field(default=None, primary_key=True)
    active: Optional[int] = Field(default=None)
    name: str = Field(max_length=100, default="")
    code: str = Field(max_length=50, default="")
    symbol: str = Field(max_length=5, default="")
    flag: Optional[int] = Field(default=None)
    rate: float = Field(default=1.0)
    rate_type: str = Field(max_length=100, default="")
    extra_fee: float = Field(default=0)
    extra_fee_type: str = Field(max_length=100, default="")
    thousand_separator: str = Field(max_length=50, default="")
    rounding: Optional[str] = Field(default="disabled", max_length=50)
    max_decimal: int = Field(default=2)
    decimal_separator: str = Field(max_length=50, default="")
    symbol_position: str = Field(max_length=50, default="")
    disable_payment_gateways: str = Field(default="")
    geo_countries_status: Optional[str] = Field(default="disable", max_length=50)
    disable_countries: Optional[str] = Field(default=None)
    welcome_country: Optional[str] = Field(default=None, max_length=50)


# =============================================================================
# Skrill Payment Models
# =============================================================================

class SkrillTransactionLog(SQLModel, table=True):
    """Skrill transaction log (8jH_skrill_transaction_log)"""
    __tablename__ = "8jH_skrill_transaction_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(default=0)
    transaction_id: Optional[str] = Field(default=None, max_length=100)
    mb_transaction_id: str = Field(max_length=50, default="")
    payment_method_id: Optional[str] = Field(default=None, max_length=30)
    payment_type: str = Field(max_length=16, default="")
    payment_status: Optional[str] = Field(default=None, max_length=30)
    amount: Decimal = Field(default=0)
    refunded_amount: Optional[Decimal] = Field(default=0)
    currency: str = Field(max_length=3, default="")
    customer_id: Optional[int] = Field(default=None)
    date: datetime = Field(default_factory=datetime.now)
    additional_information: Optional[str] = Field(default=None)
    payment_response: Optional[str] = Field(default=None)
    active: int = Field(default=1)


# =============================================================================
# WooCommerce Subscriptions Models
# =============================================================================

class WCSPaymentRetry(SQLModel, table=True):
    """WooCommerce Subscriptions payment retries (8jH_wcs_payment_retries)"""
    __tablename__ = "8jH_wcs_payment_retries"

    retry_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(default=0)
    status: str = Field(max_length=255, default="")
    date_gmt: Optional[datetime] = Field(default=None)
    rule_raw: Optional[str] = Field(default=None)


# =============================================================================
# WC Admin Notes Models
# =============================================================================

class WCAdminNote(SQLModel, table=True):
    """WC Admin notes (8jH_wc_admin_notes)"""
    __tablename__ = "8jH_wc_admin_notes"

    note_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, default="")
    type: str = Field(max_length=20, default="")
    locale: str = Field(max_length=20, default="")
    title: str = Field(default="")
    content: str = Field(default="")
    content_data: Optional[str] = Field(default=None)
    status: str = Field(max_length=200, default="")
    source: str = Field(max_length=200, default="")
    date_created: Optional[datetime] = Field(default=None)
    date_reminder: Optional[datetime] = Field(default=None)
    is_snoozable: int = Field(default=0)
    layout: str = Field(max_length=20, default="")
    image: Optional[str] = Field(default=None, max_length=200)
    is_deleted: int = Field(default=0)
    icon: str = Field(max_length=200, default="info")
    is_read: int = Field(default=0)


class WCAdminNoteAction(SQLModel, table=True):
    """WC Admin note actions (8jH_wc_admin_note_actions)"""
    __tablename__ = "8jH_wc_admin_note_actions"

    action_id: Optional[int] = Field(default=None, primary_key=True)
    note_id: int = Field(default=0, foreign_key="8jH_wc_admin_notes.note_id")
    name: str = Field(max_length=255, default="")
    label: str = Field(max_length=255, default="")
    query: str = Field(default="")
    status: str = Field(max_length=255, default="")
    actioned_text: str = Field(max_length=255, default="")
    nonce_action: Optional[str] = Field(default=None, max_length=255)
    nonce_name: Optional[str] = Field(default=None, max_length=255)


# =============================================================================
# WP File Manager Models
# =============================================================================

class WPFMBackup(SQLModel, table=True):
    """WP File Manager backup (8jH_wpfm_backup)"""
    __tablename__ = "8jH_wpfm_backup"

    id: Optional[int] = Field(default=None, primary_key=True)
    backup_name: Optional[str] = Field(default=None)
    backup_date: Optional[str] = Field(default=None)


# =============================================================================
# Quads Ad Plugin Models
# =============================================================================

class QuadsStats(SQLModel, table=True):
    """Quads ad statistics (8jH_quads_stats)"""
    __tablename__ = "8jH_quads_stats"

    id: Optional[int] = Field(default=None, primary_key=True)
    ad_id: int = Field(default=0)
    ad_thetime: int = Field(default=0)
    ad_clicks: int = Field(default=0)
    ad_impressions: int = Field(default=0)
    ad_device_name: str = Field(max_length=20, default="")
    ip_address: str = Field(max_length=20, default="")
    URL: str = Field(max_length=255, default="")
    browser: str = Field(max_length=20, default="")
    referrer: str = Field(max_length=255, default="")


# =============================================================================
# OC SMS Plugin Models
# =============================================================================

class OCRecipientsImport(SQLModel, table=True):
    """OC SMS recipients import (8jH_oc_recipients_import)"""
    __tablename__ = "8jH_oc_recipients_import"

    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: int = Field(default=0)
    country_code: int = Field(default=0)
    post_id: int = Field(default=0)
