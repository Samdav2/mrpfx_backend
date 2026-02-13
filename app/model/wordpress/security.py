"""
Security plugin database models.
Includes Wordfence, iThemes Security, BlogVault, and Loginizer.
Maps to tables with prefixes 8jH_wf*, 8jH_itsec_*, 8jH_bv_*, 8jH_loginizer_*
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


# =============================================================================
# Wordfence Models
# =============================================================================

class WFConfig(SQLModel, table=True):
    """Wordfence configuration (8jH_wfconfig)"""
    __tablename__ = "8jH_wfconfig"

    name: str = Field(primary_key=True, max_length=100)
    val: Optional[bytes] = Field(default=None)
    autoload: str = Field(max_length=3, default="yes")


class WFBlocks(SQLModel, table=True):
    """Wordfence IP blocks (8jH_wfblocks7)"""
    __tablename__ = "8jH_wfblocks7"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: int = Field(default=0)
    IP: bytes = Field(default=b'\x00' * 16)
    blockedTime: int = Field(default=0)
    reason: str = Field(max_length=255, default="")
    lastAttempt: Optional[int] = Field(default=0)
    blockedHits: Optional[int] = Field(default=0)
    expiration: int = Field(default=0)
    parameters: Optional[str] = Field(default=None)


class WFHits(SQLModel, table=True):
    """Wordfence traffic hits (8jH_wfhits)"""
    __tablename__ = "8jH_wfhits"

    id: Optional[int] = Field(default=None, primary_key=True)
    attackLogTime: float = Field(default=0)
    ctime: float = Field(default=0)
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


class WFLogins(SQLModel, table=True):
    """Wordfence login attempts (8jH_wflogins)"""
    __tablename__ = "8jH_wflogins"

    id: Optional[int] = Field(default=None, primary_key=True)
    hitID: Optional[int] = Field(default=None)
    ctime: float = Field(default=0)
    fail: int = Field(default=0)
    action: str = Field(max_length=40, default="")
    username: str = Field(max_length=255, default="")
    userID: int = Field(default=0)
    IP: Optional[bytes] = Field(default=None)
    UA: Optional[str] = Field(default=None)


class WFIssues(SQLModel, table=True):
    """Wordfence security issues (8jH_wfissues)"""
    __tablename__ = "8jH_wfissues"

    id: Optional[int] = Field(default=None, primary_key=True)
    time: int = Field(default=0)
    lastUpdated: int = Field(default=0)
    status: str = Field(max_length=10, default="")
    type: str = Field(max_length=20, default="")
    severity: int = Field(default=0)
    ignoreP: str = Field(max_length=32, default="")
    ignoreC: str = Field(max_length=32, default="")
    shortMsg: str = Field(max_length=255, default="")
    longMsg: Optional[str] = Field(default=None)
    data: Optional[str] = Field(default=None)


class WFStatus(SQLModel, table=True):
    """Wordfence status messages (8jH_wfstatus)"""
    __tablename__ = "8jH_wfstatus"

    id: Optional[int] = Field(default=None, primary_key=True)
    ctime: float = Field(default=0)
    level: int = Field(default=0)
    type: str = Field(max_length=5, default="")
    msg: str = Field(max_length=1000, default="")


class WFNotifications(SQLModel, table=True):
    """Wordfence notifications (8jH_wfnotifications)"""
    __tablename__ = "8jH_wfnotifications"

    id: str = Field(primary_key=True, max_length=32, default="")
    new: int = Field(default=1)
    category: str = Field(max_length=255, default="")
    priority: int = Field(default=1000)
    ctime: int = Field(default=0)
    html: str = Field(default="")
    links: str = Field(default="")


class WFSecurityEvents(SQLModel, table=True):
    """Wordfence security events (8jH_wfsecurityevents)"""
    __tablename__ = "8jH_wfsecurityevents"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: str = Field(max_length=255, default="")
    data: str = Field(default="")
    event_time: float = Field(default=0)
    state: str = Field(max_length=10, default="new")
    state_timestamp: Optional[datetime] = Field(default=None)


class WFLockouts(SQLModel, table=True):
    """Wordfence lockouts (8jH_wflocs)"""
    __tablename__ = "8jH_wflocs"

    IP: bytes = Field(primary_key=True, default=b'\x00' * 16)
    ctime: int = Field(default=0)
    failed: int = Field(default=0)
    city: Optional[str] = Field(default="", max_length=255)
    region: Optional[str] = Field(default="", max_length=255)
    countryName: Optional[str] = Field(default="", max_length=255)
    countryCode: Optional[str] = Field(default="", max_length=2)
    lat: Optional[float] = Field(default=0)
    lon: Optional[float] = Field(default=0)


# =============================================================================
# iThemes Security Models
# =============================================================================

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


class ITSecLog(SQLModel, table=True):
    """iThemes Security logs (8jH_itsec_logs)"""
    __tablename__ = "8jH_itsec_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    parent_id: int = Field(default=0)
    module: str = Field(max_length=50, default="")
    code: str = Field(max_length=100, default="")
    data: str = Field(default="")
    type: str = Field(max_length=20, default="notice")
    timestamp: Optional[datetime] = Field(default=None)
    init_timestamp: Optional[datetime] = Field(default=None)
    memory_current: int = Field(default=0)
    memory_peak: int = Field(default=0)
    url: str = Field(max_length=500, default="")
    blog_id: int = Field(default=0)
    user_id: int = Field(default=0)
    remote_ip: str = Field(max_length=50, default="")


class ITSecFingerprint(SQLModel, table=True):
    """iThemes Security fingerprints (8jH_itsec_fingerprints)"""
    __tablename__ = "8jH_itsec_fingerprints"

    fingerprint_id: Optional[int] = Field(default=None, primary_key=True)
    fingerprint_user: int = Field(default=0)
    fingerprint_hash: str = Field(max_length=32, default="")
    fingerprint_created_at: datetime = Field(default_factory=datetime.now)
    fingerprint_approved_at: datetime = Field(default_factory=datetime.now)
    fingerprint_data: str = Field(default="")
    fingerprint_snapshot: str = Field(default="")
    fingerprint_last_seen: datetime = Field(default_factory=datetime.now)
    fingerprint_uses: int = Field(default=0)
    fingerprint_status: str = Field(max_length=20, default="")
    fingerprint_uuid: str = Field(max_length=36, default="")


class ITSecVulnerability(SQLModel, table=True):
    """iThemes Security vulnerabilities (8jH_itsec_vulnerabilities)"""
    __tablename__ = "8jH_itsec_vulnerabilities"

    id: str = Field(primary_key=True, max_length=128)
    software_type: str = Field(max_length=20, default="")
    software_slug: str = Field(max_length=255, default="")
    first_seen: datetime = Field(default_factory=datetime.now)
    last_seen: datetime = Field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = Field(default=None)
    resolved_by: int = Field(default=0)
    resolution: str = Field(max_length=20, default="")
    details: str = Field(default="")


class ITSecDashboardEvent(SQLModel, table=True):
    """iThemes Security dashboard events (8jH_itsec_dashboard_events)"""
    __tablename__ = "8jH_itsec_dashboard_events"

    event_id: Optional[int] = Field(default=None, primary_key=True)
    event_slug: str = Field(max_length=128, default="")
    event_time: datetime = Field(default_factory=datetime.now)
    event_count: int = Field(default=1)
    event_consolidated: int = Field(default=0)


class ITSecFirewallRule(SQLModel, table=True):
    """iThemes Security firewall rules (8jH_itsec_firewall_rules)"""
    __tablename__ = "8jH_itsec_firewall_rules"

    id: Optional[int] = Field(default=None, primary_key=True)
    provider: str = Field(max_length=20, default="")
    provider_ref: str = Field(max_length=128, default="")
    name: str = Field(max_length=255, default="")
    vulnerability: str = Field(max_length=128, default="")
    config: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.now)
    paused_at: Optional[datetime] = Field(default=None)


# =============================================================================
# BlogVault/MalCare Models
# =============================================================================

class BVActivityStore(SQLModel, table=True):
    """BlogVault activities (8jH_bv_activities_store)"""
    __tablename__ = "8jH_bv_activities_store"

    id: Optional[int] = Field(default=None, primary_key=True)
    site_id: int = Field(default=0)
    user_id: Optional[int] = Field(default=0)
    username: Optional[str] = Field(default=None)
    request_id: Optional[str] = Field(default=None)
    ip: Optional[str] = Field(default="", max_length=50)
    event_type: str = Field(max_length=60, default="")
    event_data: str = Field(default="")
    time: Optional[int] = Field(default=None)


class BVFWRequest(SQLModel, table=True):
    """BlogVault firewall requests (8jH_bv_fw_requests)"""
    __tablename__ = "8jH_bv_fw_requests"

    id: Optional[int] = Field(default=None, primary_key=True)
    ip: str = Field(max_length=50, default="")
    status: int = Field(default=0)
    time: int = Field(default=0)
    path: str = Field(max_length=100, default="")
    host: str = Field(max_length=100, default="")
    method: str = Field(max_length=100, default="")
    resp_code: int = Field(default=0)
    category: int = Field(default=4)
    referer: str = Field(max_length=200, default="")
    user_agent: str = Field(max_length=200, default="")
    filenames: Optional[str] = Field(default=None)
    query_string: Optional[str] = Field(default=None)
    rules_info: Optional[str] = Field(default=None)
    request_id: Optional[str] = Field(default=None, max_length=200)
    matched_rules: Optional[str] = Field(default=None)


class BVIPStore(SQLModel, table=True):
    """BlogVault IP store (8jH_bv_ip_store)"""
    __tablename__ = "8jH_bv_ip_store"

    id: Optional[int] = Field(default=None, primary_key=True)
    start_ip_range: bytes = Field(default=b'')
    end_ip_range: bytes = Field(default=b'')
    is_fw: int = Field(default=0)
    is_lp: int = Field(default=0)
    type: int = Field(default=0)
    is_v6: int = Field(default=0)


class BVLPRequest(SQLModel, table=True):
    """BlogVault login protection requests (8jH_bv_lp_requests)"""
    __tablename__ = "8jH_bv_lp_requests"

    id: Optional[int] = Field(default=None, primary_key=True)
    ip: str = Field(max_length=50, default="")
    status: int = Field(default=0)
    username: str = Field(max_length=50, default="")
    message: str = Field(max_length=100, default="")
    category: int = Field(default=0)
    time: int = Field(default=0)
    request_id: Optional[str] = Field(default=None, max_length=200)


# =============================================================================
# Loginizer Models
# =============================================================================

class LoginizerLog(SQLModel, table=True):
    """Loginizer login logs (8jH_loginizer_logs)"""
    __tablename__ = "8jH_loginizer_logs"

    ip: str = Field(primary_key=True, max_length=255, default="")
    username: str = Field(max_length=255, default="")
    time: int = Field(default=0)
    count: int = Field(default=0)
    lockout: int = Field(default=0)
    url: str = Field(max_length=255, default="")
