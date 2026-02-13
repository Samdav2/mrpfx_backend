"""
Security API endpoints.
Exposes Wordfence, iThemes Security, BlogVault, and Loginizer data.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from pydantic import BaseModel

from app.db.session import get_session
from app.repo.wordpress.security import SecurityRepository

router = APIRouter()


# =============================================================================
# Request/Response Models
# =============================================================================

class BlockIPRequest(BaseModel):
    ip: str
    reason: str
    duration_hours: int = 24


class UpdateIssueRequest(BaseModel):
    status: str  # "new", "ignoreP", "ignoreC"


# =============================================================================
# Wordfence - Blocked IPs
# =============================================================================

@router.get("/blocks", tags=["Security - Blocks"])
async def get_blocked_ips(
    active_only: bool = True,
    limit: int = Query(100, le=500),
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get list of blocked IP addresses from Wordfence."""
    repo = SecurityRepository(session)
    return await repo.get_blocked_ips(active_only=active_only, limit=limit, offset=offset)


@router.post("/blocks", tags=["Security - Blocks"])
async def block_ip(
    request: BlockIPRequest,
    session: Session = Depends(get_session)
):
    """Block an IP address."""
    repo = SecurityRepository(session)
    return await repo.block_ip(
        ip=request.ip,
        reason=request.reason,
        duration_hours=request.duration_hours
    )


@router.delete("/blocks/{block_id}", tags=["Security - Blocks"])
async def unblock_ip(
    block_id: int,
    session: Session = Depends(get_session)
):
    """Remove an IP block."""
    repo = SecurityRepository(session)
    success = await repo.unblock_ip(block_id)
    if not success:
        raise HTTPException(status_code=404, detail="Block not found")
    return {"success": True, "message": "IP unblocked"}


# =============================================================================
# Wordfence - Login Attempts
# =============================================================================

@router.get("/logins", tags=["Security - Logins"])
async def get_login_attempts(
    failed_only: bool = False,
    username: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get login attempt logs from Wordfence."""
    repo = SecurityRepository(session)
    return await repo.get_login_attempts(
        failed_only=failed_only,
        username=username,
        limit=limit,
        offset=offset
    )


# =============================================================================
# Wordfence - Security Issues
# =============================================================================

@router.get("/issues", tags=["Security - Issues"])
async def get_security_issues(
    status: Optional[str] = None,
    severity: Optional[int] = None,
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get security issues from Wordfence."""
    repo = SecurityRepository(session)
    return await repo.get_security_issues(status=status, severity=severity, limit=limit)


@router.patch("/issues/{issue_id}", tags=["Security - Issues"])
async def update_issue_status(
    issue_id: int,
    request: UpdateIssueRequest,
    session: Session = Depends(get_session)
):
    """Update security issue status."""
    repo = SecurityRepository(session)
    success = await repo.update_issue_status(issue_id, request.status)
    if not success:
        raise HTTPException(status_code=404, detail="Issue not found")
    return {"success": True}


# =============================================================================
# Wordfence - Security Events
# =============================================================================

@router.get("/events", tags=["Security - Events"])
async def get_security_events(
    event_type: Optional[str] = None,
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get recent security events from Wordfence."""
    repo = SecurityRepository(session)
    return await repo.get_security_events(event_type=event_type, limit=limit)


# =============================================================================
# Wordfence - Traffic Hits
# =============================================================================

@router.get("/traffic", tags=["Security - Traffic"])
async def get_traffic_hits(
    attacks_only: bool = False,
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get traffic hits from Wordfence."""
    repo = SecurityRepository(session)
    return await repo.get_traffic_hits(is_attack=attacks_only, limit=limit)


# =============================================================================
# iThemes Security
# =============================================================================

@router.get("/itsec/bans", tags=["Security - iThemes"])
async def get_itsec_bans(
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get iThemes Security bans."""
    repo = SecurityRepository(session)
    return await repo.get_itsec_bans(limit=limit)


@router.get("/itsec/lockouts", tags=["Security - iThemes"])
async def get_itsec_lockouts(
    active_only: bool = True,
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get iThemes Security lockouts."""
    repo = SecurityRepository(session)
    return await repo.get_itsec_lockouts(active_only=active_only, limit=limit)


@router.get("/itsec/logs", tags=["Security - iThemes"])
async def get_itsec_logs(
    module: Optional[str] = None,
    log_type: Optional[str] = None,
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get iThemes Security logs."""
    repo = SecurityRepository(session)
    return await repo.get_itsec_logs(module=module, log_type=log_type, limit=limit)


# =============================================================================
# BlogVault
# =============================================================================

@router.get("/blogvault/activities", tags=["Security - BlogVault"])
async def get_bv_activities(
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get BlogVault activity logs."""
    repo = SecurityRepository(session)
    return await repo.get_bv_activities(limit=limit)


@router.get("/blogvault/firewall", tags=["Security - BlogVault"])
async def get_bv_firewall_requests(
    blocked_only: bool = False,
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get BlogVault firewall requests."""
    repo = SecurityRepository(session)
    return await repo.get_bv_firewall_requests(blocked_only=blocked_only, limit=limit)


# =============================================================================
# Loginizer
# =============================================================================

@router.get("/loginizer", tags=["Security - Loginizer"])
async def get_loginizer_logs(
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get Loginizer login logs."""
    repo = SecurityRepository(session)
    return await repo.get_loginizer_logs(limit=limit)


# =============================================================================
# Security Dashboard
# =============================================================================

@router.get("/stats", tags=["Security - Dashboard"])
async def get_security_stats(
    session: Session = Depends(get_session)
):
    """Get security dashboard statistics."""
    repo = SecurityRepository(session)
    return await repo.get_security_stats()
