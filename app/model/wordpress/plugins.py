"""
Various WordPress plugin database models.
Includes: Yoast SEO, Hustle, Wordfence, Action Scheduler, etc.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field


# ============== YOAST SEO ==============

class YoastIndexable(SQLModel, table=True):
    """Yoast SEO indexable (8jH_yoast_indexable)"""
    __tablename__ = "8jH_yoast_indexable"

    id: Optional[int] = Field(default=None, primary_key=True)
    permalink: Optional[str] = Field(default=None)
    permalink_hash: Optional[str] = Field(default=None, max_length=40)
    object_id: Optional[int] = Field(default=None)
    object_type: str = Field(max_length=32, default="")
    object_sub_type: Optional[str] = Field(default=None, max_length=32)
    author_id: Optional[int] = Field(default=None)
    post_parent: Optional[int] = Field(default=None)
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    breadcrumb_title: Optional[str] = Field(default=None)
    post_status: Optional[str] = Field(default=None, max_length=20)
    is_public: Optional[bool] = Field(default=None)
    is_protected: Optional[bool] = Field(default=False)
    has_public_posts: Optional[bool] = Field(default=None)
    is_robots_noindex: Optional[bool] = Field(default=False)
    is_robots_nofollow: Optional[bool] = Field(default=False)
    primary_focus_keyword: Optional[str] = Field(default=None, max_length=191)
    primary_focus_keyword_score: Optional[int] = Field(default=None)
    readability_score: Optional[int] = Field(default=None)
    is_cornerstone: Optional[bool] = Field(default=False)


class YoastSEOLink(SQLModel, table=True):
    """Yoast SEO links (8jH_yoast_seo_links)"""
    __tablename__ = "8jH_yoast_seo_links"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: Optional[str] = Field(default=None, max_length=255)
    post_id: Optional[int] = Field(default=None)
    target_post_id: Optional[int] = Field(default=None)
    type: Optional[str] = Field(default=None, max_length=8)
    indexable_id: Optional[int] = Field(default=None)
    target_indexable_id: Optional[int] = Field(default=None)


# ============== HUSTLE (Popups/Marketing) ==============

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
    """Hustle entries (8jH_hustle_entries)"""
    __tablename__ = "8jH_hustle_entries"

    entry_id: Optional[int] = Field(default=None, primary_key=True)
    entry_type: str = Field(max_length=191, default="")
    module_id: int = Field(foreign_key="8jH_hustle_modules.module_id")
    date_created: datetime = Field(default_factory=datetime.now)


class HustleEntryMeta(SQLModel, table=True):
    """Hustle entry meta (8jH_hustle_entries_meta)"""
    __tablename__ = "8jH_hustle_entries_meta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: int = Field(foreign_key="8jH_hustle_entries.entry_id")
    meta_key: Optional[str] = Field(default=None, max_length=191)
    meta_value: Optional[str] = Field(default=None)
    date_created: datetime = Field(default_factory=datetime.now)
    date_updated: datetime = Field(default_factory=datetime.now)


class HustleTracking(SQLModel, table=True):
    """Hustle tracking (8jH_hustle_tracking)"""
    __tablename__ = "8jH_hustle_tracking"

    tracking_id: Optional[int] = Field(default=None, primary_key=True)
    module_id: int = Field(foreign_key="8jH_hustle_modules.module_id")
    page_id: int = Field(default=0)
    module_type: str = Field(max_length=100, default="")
    action: str = Field(max_length=100, default="")
    ip: Optional[str] = Field(default=None, max_length=191)
    counter: int = Field(default=1)
    date_created: datetime = Field(default_factory=datetime.now)
    date_updated: datetime = Field(default_factory=datetime.now)


# ============== ACTION SCHEDULER ==============

class ActionSchedulerAction(SQLModel, table=True):
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
    extended_args: Optional[str] = Field(default=None)
    priority: int = Field(default=10)


class ActionSchedulerGroup(SQLModel, table=True):
    """Action Scheduler groups (8jH_actionscheduler_groups)"""
    __tablename__ = "8jH_actionscheduler_groups"

    group_id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(max_length=255, default="")


class ActionSchedulerLog(SQLModel, table=True):
    """Action Scheduler logs (8jH_actionscheduler_logs)"""
    __tablename__ = "8jH_actionscheduler_logs"

    log_id: Optional[int] = Field(default=None, primary_key=True)
    action_id: int = Field(foreign_key="8jH_actionscheduler_actions.action_id")
    message: str = Field(default="")
    log_date_gmt: Optional[datetime] = Field(default=None)
    log_date_local: Optional[datetime] = Field(default=None)


# ============== WPFORMS ==============

class WPFormsPayment(SQLModel, table=True):
    """WPForms payments (8jH_wpforms_payments)"""
    __tablename__ = "8jH_wpforms_payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    form_id: int = Field(default=0)
    status: str = Field(max_length=10, default="")
    subtotal_amount: Decimal = Field(default=Decimal("0.00"))
    discount_amount: Decimal = Field(default=Decimal("0.00"))
    total_amount: Decimal = Field(default=Decimal("0.00"))
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
    is_published: bool = Field(default=True)


# ============== REDIRECTION ==============

class Redirection404(SQLModel, table=True):
    """Redirection 404 logs (8jH_redirection_404)"""
    __tablename__ = "8jH_redirection_404"

    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime = Field(default_factory=datetime.now)
    url: str = Field(default="")
    domain: Optional[str] = Field(default=None, max_length=255)
    agent: Optional[str] = Field(default=None, max_length=255)
    referrer: Optional[str] = Field(default=None, max_length=255)
    http_code: int = Field(default=0)
    request_method: Optional[str] = Field(default=None, max_length=10)
    request_data: Optional[str] = Field(default=None)
    ip: Optional[str] = Field(default=None, max_length=45)


class RedirectionItem(SQLModel, table=True):
    """Redirection items (8jH_redirection_items)"""
    __tablename__ = "8jH_redirection_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(default="")
    match_url: Optional[str] = Field(default=None)
    match_data: Optional[str] = Field(default=None)
    regex: int = Field(default=0)
    position: int = Field(default=0)
    last_count: int = Field(default=0)
    last_access: datetime = Field(default_factory=datetime.now)
    group_id: int = Field(default=0)
    status: str = Field(max_length=10, default="enabled")
    action_type: str = Field(max_length=20, default="")
    action_code: int = Field(default=0)
    action_data: Optional[str] = Field(default=None)
    match_type: str = Field(max_length=20, default="")
    title: Optional[str] = Field(default=None)


class RedirectionGroup(SQLModel, table=True):
    """Redirection groups (8jH_redirection_groups)"""
    __tablename__ = "8jH_redirection_groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, default="")
    tracking: int = Field(default=1)
    module_id: int = Field(default=0)
    status: str = Field(max_length=10, default="enabled")
    position: int = Field(default=0)


# ============== ELEMENTOR ==============

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
    is_read: bool = Field(default=False)
    meta: Optional[str] = Field(default=None)
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


class WPFormsPaymentMeta(SQLModel, table=True):
    """WPForms payment meta (8jH_wpforms_payment_meta)"""
    __tablename__ = "8jH_wpforms_payment_meta"

    id: Optional[int] = Field(default=None, primary_key=True)
    payment_id: int = Field(default=0)
    meta_key: Optional[str] = Field(default=None, max_length=255)
    meta_value: Optional[str] = Field(default=None)


class WPFormsTaskMeta(SQLModel, table=True):
    """WPForms task meta (8jH_wpforms_tasks_meta)"""
    __tablename__ = "8jH_wpforms_tasks_meta"

    id: Optional[int] = Field(default=None, primary_key=True)
    action: str = Field(max_length=255, default="")
    data: str = Field(default="")
    date: datetime = Field(default_factory=datetime.now)


# ============== WORDFENCE ==============

class WFBlock(SQLModel, table=True):
    """Wordfence blocks (8jH_wfblocks7)"""
    __tablename__ = "8jH_wfblocks7"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: int = Field(default=0)
    IP: bytes = Field(default=b"")
    blockedTime: int = Field(default=0)
    reason: str = Field(max_length=255, default="")
    lastAttempt: Optional[int] = Field(default=0)
    blockedHits: Optional[int] = Field(default=0)
    expiration: int = Field(default=0)
    parameters: Optional[str] = Field(default=None)


class WFConfig(SQLModel, table=True):
    """Wordfence config (8jH_wfconfig)"""
    __tablename__ = "8jH_wfconfig"

    name: str = Field(primary_key=True, max_length=100)
    val: Optional[bytes] = Field(default=None)
    autoload: str = Field(max_length=3, default="yes")


class WFHit(SQLModel, table=True):
    """Wordfence hits (8jH_wfhits)"""
    __tablename__ = "8jH_wfhits"

    id: Optional[int] = Field(default=None, primary_key=True)
    attackLogTime: float = Field(default=0.0)
    ctime: float = Field(default=0.0)
    IP: Optional[bytes] = Field(default=None)
    jsRun: Optional[int] = Field(default=0)
    statusCode: int = Field(default=200)
    isGoogle: int = Field(default=0)
    userID: int = Field(default=0)
    newVisit: int = Field(default=0)
    URL: Optional[str] = Field(default=None)
    referer: Optional[str] = Field(default=None)
    UA: Optional[str] = Field(default=None)
    action: str = Field(max_length=64, default="")
    actionDescription: Optional[str] = Field(default=None)
    actionData: Optional[str] = Field(default=None)


class WFLogin(SQLModel, table=True):
    """Wordfence logins (8jH_wflogins)"""
    __tablename__ = "8jH_wflogins"

    id: Optional[int] = Field(default=None, primary_key=True)
    hitID: Optional[int] = Field(default=None)
    ctime: float = Field(default=0.0)
    fail: int = Field(default=0)
    action: str = Field(max_length=40, default="")
    username: str = Field(max_length=255, default="")
    userID: int = Field(default=0)
    IP: Optional[bytes] = Field(default=None)
    UA: Optional[str] = Field(default=None)


class WFStatus(SQLModel, table=True):
    """Wordfence status (8jH_wfstatus)"""
    __tablename__ = "8jH_wfstatus"

    id: Optional[int] = Field(default=None, primary_key=True)
    ctime: float = Field(default=0.0)
    level: int = Field(default=0)
    type: str = Field(max_length=5, default="")
    msg: str = Field(max_length=1000, default="")


# ============== ITHEMES SECURITY ==============

class ITSecLog(SQLModel, table=True):
    """iThemes Security logs (8jH_itsec_logs)"""
    __tablename__ = "8jH_itsec_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    parent_id: int = Field(default=0)
    module: str = Field(max_length=50, default="")
    code: str = Field(max_length=100, default="")
    data: str = Field(default="")
    type: str = Field(max_length=20, default="notice")
    timestamp: datetime = Field(default_factory=datetime.now)
    init_timestamp: datetime = Field(default_factory=datetime.now)
    memory_current: int = Field(default=0)
    memory_peak: int = Field(default=0)
    url: str = Field(max_length=500, default="")
    blog_id: int = Field(default=0)
    user_id: int = Field(default=0)
    remote_ip: str = Field(max_length=50, default="")


class ITSecLockout(SQLModel, table=True):
    """iThemes Security lockouts (8jH_itsec_lockouts)"""
    __tablename__ = "8jH_itsec_lockouts"

    lockout_id: Optional[int] = Field(default=None, primary_key=True)
    lockout_type: str = Field(max_length=25, default="")
    lockout_start: datetime = Field(default_factory=datetime.now)
    lockout_start_gmt: datetime = Field(default_factory=datetime.now)
    lockout_expire: datetime = Field(default_factory=datetime.now)
    lockout_expire_gmt: datetime = Field(default_factory=datetime.now)
    lockout_host: Optional[str] = Field(default=None, max_length=40)
    lockout_user: Optional[int] = Field(default=None)
    lockout_username: Optional[str] = Field(default=None, max_length=60)
    lockout_active: int = Field(default=1)
    lockout_context: Optional[str] = Field(default=None)


class ITSecBan(SQLModel, table=True):
    """iThemes Security bans (8jH_itsec_bans)"""
    __tablename__ = "8jH_itsec_bans"

    id: Optional[int] = Field(default=None, primary_key=True)
    host: str = Field(max_length=64, default="")
    type: str = Field(max_length=20, default="ip")
    created_at: datetime = Field(default_factory=datetime.now)
    actor_type: Optional[str] = Field(default=None, max_length=20)
    actor_id: Optional[str] = Field(default=None, max_length=128)
    comment: str = Field(max_length=255, default="")
