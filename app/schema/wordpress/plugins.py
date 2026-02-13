"""
WordPress Plugin Pydantic Schemas
Schemas for Yoast SEO, Hustle Marketing, Action Scheduler, and other plugins.
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


# ============== Yoast SEO Schemas ==============

class YoastSEOMeta(BaseModel):
    """Yoast SEO metadata for a post"""
    post_id: int
    focus_keyword: Optional[str] = None
    seo_title: Optional[str] = None
    meta_description: Optional[str] = None
    canonical_url: Optional[str] = None
    is_cornerstone: bool = False
    is_robots_noindex: bool = False
    is_robots_nofollow: bool = False
    primary_category_id: Optional[int] = None
    schema_page_type: Optional[str] = None
    schema_article_type: Optional[str] = None

    class Config:
        from_attributes = True


class YoastIndexableRead(BaseModel):
    """Yoast SEO indexable entry"""
    id: int
    permalink: Optional[str] = None
    object_id: Optional[int] = None
    object_type: str = ""
    object_sub_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    breadcrumb_title: Optional[str] = None
    is_cornerstone: bool = False
    link_count: int = 0
    incoming_link_count: int = 0

    class Config:
        from_attributes = True


# ============== Action Scheduler Schemas ==============

class ActionSchedulerAction(BaseModel):
    """Action Scheduler action schema"""
    action_id: int
    hook: str
    status: str
    scheduled_date_gmt: Optional[datetime] = None
    scheduled_date_local: Optional[datetime] = None
    args: Optional[str] = None
    schedule: Optional[str] = None
    group_id: int = 0
    attempts: int = 0
    last_attempt_gmt: Optional[datetime] = None
    last_attempt_local: Optional[datetime] = None
    claim_id: int = 0
    priority: int = 10

    class Config:
        from_attributes = True


class ActionSchedulerGroup(BaseModel):
    """Action Scheduler group schema"""
    group_id: int
    slug: str

    class Config:
        from_attributes = True


class ActionSchedulerLog(BaseModel):
    """Action Scheduler log schema"""
    log_id: int
    action_id: int
    message: str
    log_date_gmt: Optional[datetime] = None
    log_date_local: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============== Hustle Marketing Schemas ==============

class HustleModule(BaseModel):
    """Hustle marketing module schema"""
    module_id: int
    blog_id: int = 0
    module_name: str
    module_type: str
    active: int = 1
    module_mode: str

    class Config:
        from_attributes = True


class HustleModuleMeta(BaseModel):
    """Hustle module meta schema"""
    meta_id: int
    module_id: int
    meta_key: Optional[str] = None
    meta_value: Optional[str] = None

    class Config:
        from_attributes = True


class HustleEntry(BaseModel):
    """Hustle form entry schema"""
    entry_id: int
    entry_type: str
    module_id: int
    date_created: datetime

    class Config:
        from_attributes = True


class HustleEntryMeta(BaseModel):
    """Hustle entry meta schema"""
    meta_id: int
    entry_id: int
    meta_key: Optional[str] = None
    meta_value: Optional[str] = None
    date_created: datetime
    date_updated: datetime

    class Config:
        from_attributes = True


class HustleTracking(BaseModel):
    """Hustle tracking schema for analytics"""
    tracking_id: int
    module_id: int
    page_id: int
    module_type: str
    action: str
    ip: Optional[str] = None
    counter: int = 1
    date_created: datetime
    date_updated: datetime

    class Config:
        from_attributes = True


# ============== Elementor Schemas ==============

class ElementorEvent(BaseModel):
    """Elementor event schema"""
    id: int
    event_data: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ElementorNote(BaseModel):
    """Elementor notes schema"""
    id: int
    route_url: Optional[str] = None
    route_title: Optional[str] = None
    route_post_id: Optional[int] = None
    post_id: Optional[int] = None
    element_id: Optional[str] = None
    parent_id: int = 0
    author_id: Optional[int] = None
    author_display_name: Optional[str] = None
    status: str = "publish"
    position: Optional[str] = None
    content: Optional[str] = None
    is_resolved: bool = False
    is_public: bool = True
    last_activity_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ElementorSubmission(BaseModel):
    """Elementor form submission schema"""
    id: int
    type: Optional[str] = None
    hash_id: str
    main_meta_id: int
    post_id: int
    referer: str
    referer_title: Optional[str] = None
    element_id: str
    form_name: str
    campaign_id: int
    user_id: Optional[int] = None
    user_ip: str
    status: str
    is_read: bool = False
    meta: Optional[str] = None
    created_at_gmt: datetime
    updated_at_gmt: datetime

    class Config:
        from_attributes = True


# ============== WPForms Schemas ==============

class WPFormsEntry(BaseModel):
    """WPForms entry schema"""
    entry_id: int
    form_id: int
    post_id: int = 0
    user_id: int = 0
    status: str = "publish"
    type: str = ""
    viewed: bool = False
    starred: bool = False
    fields: Optional[str] = None
    meta: Optional[str] = None
    date: datetime
    date_modified: datetime
    ip_address: str = ""
    user_agent: str = ""
    user_uuid: str = ""

    class Config:
        from_attributes = True


class WPFormsEntryMeta(BaseModel):
    """WPForms entry meta schema"""
    id: int
    entry_id: int
    type: str
    data: Optional[str] = None
    date: datetime

    class Config:
        from_attributes = True


# ============== WPForms Management Schemas ==============

class WPFormCreate(BaseModel):
    """Schema for creating a new form"""
    title: str = Field(..., description="Form title")
    content: str = Field("", description="Form configuration/content")


class WPFormRead(BaseModel):
    """Schema for reading form details"""
    id: int
    title: str
    date: datetime
    type: str = "wpforms"

    class Config:
        from_attributes = True


class NewsletterSubscribe(BaseModel):
    """Schema for public newsletter subscription"""
    email: str = Field(..., description="Subscriber email")
    name: Optional[str] = Field(None, description="Subscriber name")
    form_id: Optional[int] = Field(None, description="Source form ID")


class WPFormsLogRead(BaseModel):
    """Schema for reading form submission logs (entries)"""
    id: int
    form_id: Optional[int] = None
    entry_id: Optional[int] = None
    user_id: Optional[int] = None
    title: str
    message: str
    types: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============== Redirection Schemas ==============

class Redirection404(BaseModel):
    """Redirection 404 log schema"""
    id: int
    created: datetime
    url: str
    domain: Optional[str] = None
    agent: Optional[str] = None
    referrer: Optional[str] = None
    request_method: Optional[str] = None
    request_data: Optional[str] = None
    http_code: int = 0
    ip: Optional[str] = None

    class Config:
        from_attributes = True


class RedirectionItem(BaseModel):
    """Redirection item schema"""
    id: int
    url: str
    match_url: Optional[str] = None
    match_data: Optional[str] = None
    regex: bool = False
    position: int = 0
    last_count: int = 0
    last_access: datetime
    group_id: int = 0
    status: str = "enabled"
    action_type: str = "url"
    action_code: int = 301
    action_data: Optional[str] = None
    match_type: str = "url"
    title: Optional[str] = None

    class Config:
        from_attributes = True


class RedirectionGroup(BaseModel):
    """Redirection group schema"""
    id: int
    name: str
    tracking: int = 1
    module_id: int = 0
    status: str = "enabled"
    position: int = 0

    class Config:
        from_attributes = True


class RedirectionLog(BaseModel):
    """Redirection log schema"""
    id: int
    created: datetime
    url: str
    domain: Optional[str] = None
    sent_to: Optional[str] = None
    agent: Optional[str] = None
    referrer: Optional[str] = None
    request_method: Optional[str] = None
    request_data: Optional[str] = None
    http_code: int = 0
    redirect_by: Optional[str] = None
    redirection_id: Optional[int] = None
    ip: Optional[str] = None

    class Config:
        from_attributes = True


# ============== iThemes Security Schemas ==============

class ITSecBan(BaseModel):
    """iThemes Security ban schema"""
    id: int
    host: str
    type: str = "ip"
    created_at: datetime
    actor_type: Optional[str] = None
    actor_id: Optional[str] = None
    comment: str = ""

    class Config:
        from_attributes = True


class ITSecLockout(BaseModel):
    """iThemes Security lockout schema"""
    lockout_id: int
    lockout_type: str
    lockout_start: datetime
    lockout_start_gmt: datetime
    lockout_expire: datetime
    lockout_expire_gmt: datetime
    lockout_host: Optional[str] = None
    lockout_user: Optional[int] = None
    lockout_username: Optional[str] = None
    lockout_active: int = 1
    lockout_context: Optional[str] = None

    class Config:
        from_attributes = True


class ITSecLog(BaseModel):
    """iThemes Security log schema"""
    id: int
    parent_id: int = 0
    module: str = ""
    code: str = ""
    data: str = ""
    type: str = "notice"
    timestamp: datetime
    init_timestamp: datetime
    url: str = ""
    blog_id: int = 0
    user_id: int = 0
    remote_ip: str = ""

    class Config:
        from_attributes = True
