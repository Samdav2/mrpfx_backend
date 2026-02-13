"""
Elementor page builder database models.
Maps to tables with prefix 8jH_e_*
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class ElementorEvent(SQLModel, table=True):
    """Elementor events (8jH_e_events)"""
    __tablename__ = "8jH_e_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    event_data: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)


class ElementorNote(SQLModel, table=True):
    """Elementor notes/comments (8jH_e_notes)"""
    __tablename__ = "8jH_e_notes"

    id: Optional[int] = Field(default=None, primary_key=True)
    route_url: Optional[str] = Field(default=None)
    route_title: Optional[str] = Field(default=None, max_length=255)
    route_post_id: Optional[int] = Field(default=None)
    post_id: Optional[int] = Field(default=None)
    element_id: Optional[str] = Field(default=None, max_length=60)
    parent_id: int = Field(default=0)
    author_id: Optional[int] = Field(default=None)
    author_display_name: Optional[str] = Field(default=None, max_length=250)
    status: str = Field(max_length=20, default="publish")
    position: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    is_resolved: int = Field(default=0)
    is_public: int = Field(default=1)
    last_activity_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ElementorNoteUserRelation(SQLModel, table=True):
    """Elementor note-user relations (8jH_e_notes_users_relations)"""
    __tablename__ = "8jH_e_notes_users_relations"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: str = Field(max_length=60, default="")
    note_id: int = Field(default=0, foreign_key="8jH_e_notes.id")
    user_id: int = Field(default=0, foreign_key="8jH_users.ID")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ElementorSubmission(SQLModel, table=True):
    """Elementor form submissions (8jH_e_submissions)"""
    __tablename__ = "8jH_e_submissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: Optional[str] = Field(default=None, max_length=60)
    hash_id: str = Field(max_length=60, default="")
    main_meta_id: int = Field(default=0)
    post_id: int = Field(default=0)
    referer: str = Field(max_length=500, default="")
    referer_title: Optional[str] = Field(default=None, max_length=300)
    element_id: str = Field(max_length=20, default="")
    form_name: str = Field(max_length=60, default="")
    campaign_id: int = Field(default=0)
    user_id: Optional[int] = Field(default=None)
    user_ip: str = Field(max_length=46, default="")
    user_agent: str = Field(default="")
    actions_count: Optional[int] = Field(default=0)
    actions_succeeded_count: Optional[int] = Field(default=0)
    status: str = Field(max_length=20, default="")
    is_read: int = Field(default=0)
    meta: Optional[str] = Field(default=None)
    created_at_gmt: datetime = Field(default_factory=datetime.now)
    updated_at_gmt: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ElementorSubmissionActionLog(SQLModel, table=True):
    """Elementor submission action logs (8jH_e_submissions_actions_log)"""
    __tablename__ = "8jH_e_submissions_actions_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    submission_id: int = Field(default=0, foreign_key="8jH_e_submissions.id")
    action_name: str = Field(max_length=60, default="")
    action_label: Optional[str] = Field(default=None, max_length=60)
    status: str = Field(max_length=20, default="")
    log: Optional[str] = Field(default=None)
    created_at_gmt: datetime = Field(default_factory=datetime.now)
    updated_at_gmt: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ElementorSubmissionValue(SQLModel, table=True):
    """Elementor submission values (8jH_e_submissions_values)"""
    __tablename__ = "8jH_e_submissions_values"

    id: Optional[int] = Field(default=None, primary_key=True)
    submission_id: int = Field(default=0, foreign_key="8jH_e_submissions.id")
    key: Optional[str] = Field(default=None, max_length=60)
    value: Optional[str] = Field(default=None)
