"""
Action Scheduler database models.
Used by WooCommerce for background task processing.
Maps to tables with prefix 8jH_actionscheduler_*
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class ASAction(SQLModel, table=True):
    """Action Scheduler actions (8jH_actionscheduler_actions)"""
    __tablename__ = "8jH_actionscheduler_actions"

    action_id: Optional[int] = Field(default=None, primary_key=True)
    hook: str = Field(max_length=191, default="")
    status: str = Field(max_length=20, default="")
    scheduled_date_gmt: Optional[datetime] = Field(default=None)
    scheduled_date_local: Optional[datetime] = Field(default=None)
    args: Optional[str] = Field(default=None, max_length=191)
    schedule: Optional[str] = Field(default=None)
    group_id: int = Field(default=0)
    attempts: int = Field(default=0)
    last_attempt_gmt: Optional[datetime] = Field(default=None)
    last_attempt_local: Optional[datetime] = Field(default=None)
    claim_id: int = Field(default=0)
    extended_args: Optional[str] = Field(default=None, max_length=8000)
    priority: int = Field(default=10)


class ASClaim(SQLModel, table=True):
    """Action Scheduler claims (8jH_actionscheduler_claims)"""
    __tablename__ = "8jH_actionscheduler_claims"

    claim_id: Optional[int] = Field(default=None, primary_key=True)
    date_created_gmt: datetime = Field(default_factory=datetime.now)


class ASGroup(SQLModel, table=True):
    """Action Scheduler groups (8jH_actionscheduler_groups)"""
    __tablename__ = "8jH_actionscheduler_groups"

    group_id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(max_length=255, default="")


class ASLog(SQLModel, table=True):
    """Action Scheduler logs (8jH_actionscheduler_logs)"""
    __tablename__ = "8jH_actionscheduler_logs"

    log_id: Optional[int] = Field(default=None, primary_key=True)
    action_id: int = Field(default=0, foreign_key="8jH_actionscheduler_actions.action_id")
    message: str = Field(default="")
    log_date_gmt: Optional[datetime] = Field(default=None)
    log_date_local: Optional[datetime] = Field(default=None)
