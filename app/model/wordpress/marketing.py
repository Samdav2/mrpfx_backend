"""
Marketing and lead generation plugin database models.
Includes Hustle and OptinPanda.
Maps to tables with prefixes 8jH_hustle_*, 8jH_opanda_*
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


# =============================================================================
# Hustle Models
# =============================================================================

class HustleModule(SQLModel, table=True):
    """Hustle modules (8jH_hustle_modules)"""
    __tablename__ = "8jH_hustle_modules"

    module_id: Optional[int] = Field(default=None, primary_key=True)
    blog_id: int = Field(default=0)
    module_name: str = Field(max_length=255, default="")
    module_type: str = Field(max_length=100, default="")
    active: Optional[int] = Field(default=1)
    module_mode: str = Field(max_length=100, default="")


class HustleModuleMeta(SQLModel, table=True):
    """Hustle module meta (8jH_hustle_modules_meta)"""
    __tablename__ = "8jH_hustle_modules_meta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    module_id: int = Field(default=0, foreign_key="8jH_hustle_modules.module_id")
    meta_key: Optional[str] = Field(default=None, max_length=191)
    meta_value: Optional[str] = Field(default=None)


class HustleEntry(SQLModel, table=True):
    """Hustle entries/submissions (8jH_hustle_entries)"""
    __tablename__ = "8jH_hustle_entries"

    entry_id: Optional[int] = Field(default=None, primary_key=True)
    entry_type: str = Field(max_length=191, default="")
    module_id: int = Field(default=0, foreign_key="8jH_hustle_modules.module_id")
    date_created: Optional[datetime] = Field(default=None)


class HustleEntryMeta(SQLModel, table=True):
    """Hustle entry meta (8jH_hustle_entries_meta)"""
    __tablename__ = "8jH_hustle_entries_meta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: int = Field(default=0, foreign_key="8jH_hustle_entries.entry_id")
    meta_key: Optional[str] = Field(default=None, max_length=191)
    meta_value: Optional[str] = Field(default=None)
    date_created: Optional[datetime] = Field(default=None)
    date_updated: Optional[datetime] = Field(default=None)


class HustleTracking(SQLModel, table=True):
    """Hustle tracking data (8jH_hustle_tracking)"""
    __tablename__ = "8jH_hustle_tracking"

    tracking_id: Optional[int] = Field(default=None, primary_key=True)
    module_id: int = Field(default=0, foreign_key="8jH_hustle_modules.module_id")
    page_id: int = Field(default=0)
    module_type: str = Field(max_length=100, default="")
    action: str = Field(max_length=100, default="")
    ip: Optional[str] = Field(default=None, max_length=191)
    counter: int = Field(default=1)
    date_created: Optional[datetime] = Field(default=None)
    date_updated: Optional[datetime] = Field(default=None)


# =============================================================================
# OptinPanda / Content Locker Models
# =============================================================================

class OpandaLead(SQLModel, table=True):
    """OptinPanda leads (8jH_opanda_leads)"""
    __tablename__ = "8jH_opanda_leads"

    ID: Optional[int] = Field(default=None, primary_key=True)
    lead_display_name: Optional[str] = Field(default=None, max_length=255)
    lead_name: Optional[str] = Field(default=None, max_length=100)
    lead_family: Optional[str] = Field(default=None, max_length=100)
    lead_email: str = Field(max_length=50, default="")
    lead_date: int = Field(default=0)
    lead_email_confirmed: int = Field(default=0)
    lead_subscription_confirmed: int = Field(default=0)
    lead_ip: Optional[str] = Field(default=None, max_length=45)
    lead_item_id: Optional[int] = Field(default=None)
    lead_post_id: Optional[int] = Field(default=None)
    lead_item_title: Optional[str] = Field(default=None, max_length=255)
    lead_post_title: Optional[str] = Field(default=None, max_length=255)
    lead_referer: Optional[str] = Field(default=None)
    lead_confirmation_code: Optional[str] = Field(default=None, max_length=32)
    lead_temp: Optional[str] = Field(default=None)


class OpandaLeadField(SQLModel, table=True):
    """OptinPanda lead fields (8jH_opanda_leads_fields)"""
    __tablename__ = "8jH_opanda_leads_fields"

    lead_id: int = Field(primary_key=True)
    field_name: str = Field(primary_key=True, max_length=150)
    field_value: str = Field(default="")
    field_custom: int = Field(default=0)


class OpandaStat(SQLModel, table=True):
    """OptinPanda statistics (8jH_opanda_stats_v2)"""
    __tablename__ = "8jH_opanda_stats_v2"

    ID: Optional[int] = Field(default=None, primary_key=True)
    aggregate_date: datetime = Field(default_factory=datetime.now)
    post_id: int = Field(default=0)
    item_id: int = Field(default=0)
    metric_name: str = Field(max_length=50, default="")
    metric_value: int = Field(default=0)


class MTSLockerStats(SQLModel, table=True):
    """MTS Locker statistics (8jH_mts_locker_stats)"""
    __tablename__ = "8jH_mts_locker_stats"

    ID: Optional[int] = Field(default=None, primary_key=True)
    aggregate_date: datetime = Field(default_factory=datetime.now)
    post_id: int = Field(default=0)
    locker_id: int = Field(default=0)
    metric_name: str = Field(max_length=50, default="")
    metric_value: int = Field(default=0)
