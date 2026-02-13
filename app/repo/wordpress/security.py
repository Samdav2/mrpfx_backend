"""
Security plugin repository.
Handles Wordfence, iThemes Security, BlogVault, and Loginizer data.
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select, func, desc
from sqlalchemy import text

from app.model.wordpress.security import (
    WFConfig, WFBlocks, WFHits, WFLogins, WFIssues, WFStatus,
    WFNotifications, WFSecurityEvents, WFLockouts,
    ITSecBan, ITSecLockout, ITSecLog, ITSecFingerprint,
    BVActivityStore, BVFWRequest, BVLPRequest,
    LoginizerLog
)


class SecurityRepository:
    """Repository for security plugin data access."""

    def __init__(self, session: Session):
        self.session = session

    # =========================================================================
    # Wordfence - Blocked IPs
    # =========================================================================

    async def get_blocked_ips(
        self,
        active_only: bool = True,
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """Get list of blocked IPs from Wordfence."""
        query = select(WFBlocks)

        if active_only:
            now = int(datetime.now().timestamp())
            query = query.where(WFBlocks.expiration > now)

        query = query.order_by(desc(WFBlocks.blockedTime)).offset(offset).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": block.id,
                "ip": self._bytes_to_ip(block.IP) if block.IP else None,
                "blocked_time": datetime.fromtimestamp(block.blockedTime) if block.blockedTime else None,
                "reason": block.reason,
                "expiration": datetime.fromtimestamp(block.expiration) if block.expiration else None,
                "blocked_hits": block.blockedHits,
                "type": block.type
            }
            for block in result
        ]

    async def block_ip(
        self,
        ip: str,
        reason: str,
        duration_hours: int = 24
    ) -> dict:
        """Block an IP address."""
        now = int(datetime.now().timestamp())
        expiration = now + (duration_hours * 3600)

        block = WFBlocks(
            type=1,  # Manual block
            IP=self._ip_to_bytes(ip),
            blockedTime=now,
            reason=reason,
            expiration=expiration,
            blockedHits=0
        )
        self.session.add(block)
        self.session.commit()
        self.session.refresh(block)

        return {"id": block.id, "ip": ip, "blocked": True}

    async def unblock_ip(self, block_id: int) -> bool:
        """Remove an IP block."""
        block = self.session.get(WFBlocks, block_id)
        if block:
            self.session.delete(block)
            self.session.commit()
            return True
        return False

    # =========================================================================
    # Wordfence - Login Attempts
    # =========================================================================

    async def get_login_attempts(
        self,
        failed_only: bool = False,
        username: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """Get login attempt logs from Wordfence."""
        query = select(WFLogins)

        if failed_only:
            query = query.where(WFLogins.fail == 1)

        if username:
            query = query.where(WFLogins.username == username)

        query = query.order_by(desc(WFLogins.ctime)).offset(offset).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": login.id,
                "username": login.username,
                "user_id": login.userID,
                "ip": self._bytes_to_ip(login.IP) if login.IP else None,
                "failed": login.fail == 1,
                "action": login.action,
                "time": datetime.fromtimestamp(login.ctime) if login.ctime else None,
                "user_agent": login.UA
            }
            for login in result
        ]

    # =========================================================================
    # Wordfence - Security Issues
    # =========================================================================

    async def get_security_issues(
        self,
        status: Optional[str] = None,  # "new", "ignoreP", "ignoreC"
        severity: Optional[int] = None,
        limit: int = 100
    ) -> List[dict]:
        """Get security issues from Wordfence."""
        query = select(WFIssues)

        if status:
            query = query.where(WFIssues.status == status)

        if severity is not None:
            query = query.where(WFIssues.severity >= severity)

        query = query.order_by(desc(WFIssues.time)).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": issue.id,
                "type": issue.type,
                "severity": issue.severity,
                "status": issue.status,
                "short_message": issue.shortMsg,
                "long_message": issue.longMsg,
                "time": datetime.fromtimestamp(issue.time) if issue.time else None,
                "last_updated": datetime.fromtimestamp(issue.lastUpdated) if issue.lastUpdated else None
            }
            for issue in result
        ]

    async def update_issue_status(self, issue_id: int, status: str) -> bool:
        """Update security issue status."""
        issue = self.session.get(WFIssues, issue_id)
        if issue:
            issue.status = status
            issue.lastUpdated = int(datetime.now().timestamp())
            self.session.add(issue)
            self.session.commit()
            return True
        return False

    # =========================================================================
    # Wordfence - Security Events
    # =========================================================================

    async def get_security_events(
        self,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[dict]:
        """Get recent security events."""
        query = select(WFSecurityEvents)

        if event_type:
            query = query.where(WFSecurityEvents.type == event_type)

        query = query.order_by(desc(WFSecurityEvents.event_time)).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": event.id,
                "type": event.type,
                "data": event.data,
                "time": datetime.fromtimestamp(event.event_time) if event.event_time else None,
                "state": event.state
            }
            for event in result
        ]

    # =========================================================================
    # Wordfence - Traffic/Hits
    # =========================================================================

    async def get_traffic_hits(
        self,
        is_attack: bool = False,
        limit: int = 100
    ) -> List[dict]:
        """Get traffic hits from Wordfence."""
        query = select(WFHits)

        if is_attack:
            query = query.where(WFHits.attackLogTime > 0)

        query = query.order_by(desc(WFHits.ctime)).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": hit.id,
                "ip": self._bytes_to_ip(hit.IP) if hit.IP else None,
                "url": hit.URL,
                "status_code": hit.statusCode,
                "is_google": hit.isGoogle == 1,
                "user_id": hit.userID,
                "action": hit.action,
                "action_description": hit.actionDescription,
                "referer": hit.referer,
                "user_agent": hit.UA,
                "time": datetime.fromtimestamp(hit.ctime) if hit.ctime else None
            }
            for hit in result
        ]

    # =========================================================================
    # iThemes Security - Bans & Lockouts
    # =========================================================================

    async def get_itsec_bans(self, limit: int = 100) -> List[dict]:
        """Get iThemes Security bans."""
        query = select(ITSecBan).order_by(desc(ITSecBan.created_at)).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": ban.id,
                "host": ban.host,
                "type": ban.type,
                "created_at": ban.created_at,
                "comment": ban.comment
            }
            for ban in result
        ]

    async def get_itsec_lockouts(
        self,
        active_only: bool = True,
        limit: int = 100
    ) -> List[dict]:
        """Get iThemes Security lockouts."""
        query = select(ITSecLockout)

        if active_only:
            query = query.where(ITSecLockout.lockout_active == 1)
            query = query.where(ITSecLockout.lockout_expire_gmt > datetime.utcnow())

        query = query.order_by(desc(ITSecLockout.lockout_start)).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": lockout.lockout_id,
                "type": lockout.lockout_type,
                "host": lockout.lockout_host,
                "user": lockout.lockout_user,
                "username": lockout.lockout_username,
                "start": lockout.lockout_start,
                "expire": lockout.lockout_expire,
                "active": lockout.lockout_active == 1
            }
            for lockout in result
        ]

    async def get_itsec_logs(
        self,
        module: Optional[str] = None,
        log_type: Optional[str] = None,
        limit: int = 100
    ) -> List[dict]:
        """Get iThemes Security logs."""
        query = select(ITSecLog)

        if module:
            query = query.where(ITSecLog.module == module)
        if log_type:
            query = query.where(ITSecLog.type == log_type)

        query = query.order_by(desc(ITSecLog.timestamp)).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": log.id,
                "module": log.module,
                "code": log.code,
                "type": log.type,
                "url": log.url,
                "remote_ip": log.remote_ip,
                "user_id": log.user_id,
                "timestamp": log.timestamp
            }
            for log in result
        ]

    # =========================================================================
    # BlogVault - Activity & Firewall
    # =========================================================================

    async def get_bv_activities(self, limit: int = 100) -> List[dict]:
        """Get BlogVault activity logs."""
        query = select(BVActivityStore).order_by(desc(BVActivityStore.time)).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": activity.id,
                "event_type": activity.event_type,
                "username": activity.username,
                "ip": activity.ip,
                "time": datetime.fromtimestamp(activity.time) if activity.time else None,
                "data": activity.event_data
            }
            for activity in result
        ]

    async def get_bv_firewall_requests(
        self,
        blocked_only: bool = False,
        limit: int = 100
    ) -> List[dict]:
        """Get BlogVault firewall requests."""
        query = select(BVFWRequest)

        if blocked_only:
            query = query.where(BVFWRequest.status != 0)

        query = query.order_by(desc(BVFWRequest.time)).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": req.id,
                "ip": req.ip,
                "path": req.path,
                "method": req.method,
                "status": req.status,
                "response_code": req.resp_code,
                "category": req.category,
                "time": datetime.fromtimestamp(req.time) if req.time else None
            }
            for req in result
        ]

    # =========================================================================
    # Loginizer
    # =========================================================================

    async def get_loginizer_logs(self, limit: int = 100) -> List[dict]:
        """Get Loginizer login logs."""
        query = select(LoginizerLog).order_by(desc(LoginizerLog.time)).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "ip": log.ip,
                "username": log.username,
                "count": log.count,
                "lockout": log.lockout == 1,
                "url": log.url,
                "time": datetime.fromtimestamp(log.time) if log.time else None
            }
            for log in result
        ]

    # =========================================================================
    # Security Dashboard / Stats
    # =========================================================================

    async def get_security_stats(self) -> dict:
        """Get security dashboard statistics."""
        now = int(datetime.now().timestamp())
        day_ago = now - 86400
        week_ago = now - (86400 * 7)

        # Blocked IPs count
        blocked_count = self.session.exec(
            select(func.count()).select_from(WFBlocks).where(WFBlocks.expiration > now)
        ).one()

        # Failed logins (24h)
        failed_logins_24h = self.session.exec(
            select(func.count()).select_from(WFLogins)
            .where(WFLogins.fail == 1)
            .where(WFLogins.ctime > day_ago)
        ).one()

        # Security issues by severity
        critical_issues = self.session.exec(
            select(func.count()).select_from(WFIssues)
            .where(WFIssues.status == "new")
            .where(WFIssues.severity >= 3)
        ).one()

        # Active lockouts
        active_lockouts = self.session.exec(
            select(func.count()).select_from(ITSecLockout)
            .where(ITSecLockout.lockout_active == 1)
            .where(ITSecLockout.lockout_expire_gmt > datetime.utcnow())
        ).one()

        return {
            "blocked_ips": blocked_count,
            "failed_logins_24h": failed_logins_24h,
            "critical_issues": critical_issues,
            "active_lockouts": active_lockouts,
            "last_updated": datetime.now().isoformat()
        }

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _ip_to_bytes(self, ip: str) -> bytes:
        """Convert IP string to bytes for Wordfence storage."""
        import socket
        try:
            # Try IPv4
            return socket.inet_pton(socket.AF_INET, ip).ljust(16, b'\x00')
        except socket.error:
            try:
                # Try IPv6
                return socket.inet_pton(socket.AF_INET6, ip)
            except socket.error:
                return b'\x00' * 16

    def _bytes_to_ip(self, ip_bytes: bytes) -> str:
        """Convert bytes to IP string."""
        import socket
        if not ip_bytes:
            return ""

        # Check if it's an IPv4 address (padded with zeros)
        if ip_bytes[4:] == b'\x00' * 12:
            try:
                return socket.inet_ntop(socket.AF_INET, ip_bytes[:4])
            except (socket.error, ValueError):
                pass

        # Try as IPv6
        try:
            return socket.inet_ntop(socket.AF_INET6, ip_bytes[:16])
        except (socket.error, ValueError):
            return ""
