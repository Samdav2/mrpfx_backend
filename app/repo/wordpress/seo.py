"""
SEO plugin repository.
Handles Yoast SEO and Redirection plugin data.
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select, func, desc

from app.model.wordpress.seo import (
    YoastIndexable, YoastIndexableHierarchy, YoastPrimaryTerm, YoastSEOLink,
    RedirectionGroup, RedirectionItem, RedirectionLog, Redirection404
)


class SEORepository:
    """Repository for SEO plugin data access."""

    def __init__(self, session: Session):
        self.session = session

    # =========================================================================
    # Yoast SEO - Indexables
    # =========================================================================

    async def get_indexables(
        self,
        object_type: Optional[str] = None,  # "post", "term", "user", "home-page"
        object_sub_type: Optional[str] = None,  # "post", "page", "product"
        is_public: bool = True,
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """Get Yoast SEO indexables."""
        query = select(YoastIndexable)

        if object_type:
            query = query.where(YoastIndexable.object_type == object_type)
        if object_sub_type:
            query = query.where(YoastIndexable.object_sub_type == object_sub_type)
        if is_public:
            query = query.where(YoastIndexable.is_public == 1)

        query = query.order_by(desc(YoastIndexable.updated_at)).offset(offset).limit(limit)
        result = self.session.exec(query).all()

        return [self._indexable_to_dict(idx) for idx in result]

    async def get_post_seo(self, post_id: int) -> Optional[dict]:
        """Get SEO data for a specific post."""
        query = select(YoastIndexable).where(
            YoastIndexable.object_type == "post"
        ).where(
            YoastIndexable.object_id == post_id
        )

        result = self.session.exec(query).first()
        if result:
            return self._indexable_to_dict(result)
        return None

    async def update_post_seo(
        self,
        post_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        focus_keyword: Optional[str] = None,
        is_cornerstone: Optional[bool] = None,
        canonical: Optional[str] = None,
        og_title: Optional[str] = None,
        og_description: Optional[str] = None,
        og_image: Optional[str] = None,
        twitter_title: Optional[str] = None,
        twitter_description: Optional[str] = None
    ) -> Optional[dict]:
        """Update SEO metadata for a post."""
        query = select(YoastIndexable).where(
            YoastIndexable.object_type == "post"
        ).where(
            YoastIndexable.object_id == post_id
        )

        indexable = self.session.exec(query).first()
        if not indexable:
            return None

        if title is not None:
            indexable.title = title
        if description is not None:
            indexable.description = description
        if focus_keyword is not None:
            indexable.primary_focus_keyword = focus_keyword
        if is_cornerstone is not None:
            indexable.is_cornerstone = 1 if is_cornerstone else 0
        if canonical is not None:
            indexable.canonical = canonical
        if og_title is not None:
            indexable.open_graph_title = og_title
        if og_description is not None:
            indexable.open_graph_description = og_description
        if og_image is not None:
            indexable.open_graph_image = og_image
        if twitter_title is not None:
            indexable.twitter_title = twitter_title
        if twitter_description is not None:
            indexable.twitter_description = twitter_description

        indexable.updated_at = datetime.now()
        self.session.add(indexable)
        self.session.commit()
        self.session.refresh(indexable)

        return self._indexable_to_dict(indexable)

    async def get_seo_links(
        self,
        post_id: Optional[int] = None,
        link_type: Optional[str] = None,  # "internal", "external"
        limit: int = 100
    ) -> List[dict]:
        """Get SEO internal/external links."""
        query = select(YoastSEOLink)

        if post_id:
            query = query.where(YoastSEOLink.post_id == post_id)
        if link_type:
            query = query.where(YoastSEOLink.type == link_type)

        query = query.limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": link.id,
                "url": link.url,
                "post_id": link.post_id,
                "target_post_id": link.target_post_id,
                "type": link.type
            }
            for link in result
        ]

    # =========================================================================
    # Redirection Plugin
    # =========================================================================

    async def get_redirect_groups(self) -> List[dict]:
        """Get redirect groups."""
        query = select(RedirectionGroup).order_by(RedirectionGroup.position)
        result = self.session.exec(query).all()

        return [
            {
                "id": group.id,
                "name": group.name,
                "status": group.status,
                "tracking": group.tracking == 1
            }
            for group in result
        ]

    async def get_redirects(
        self,
        group_id: Optional[int] = None,
        status: str = "enabled",
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """Get redirect items."""
        query = select(RedirectionItem)

        if group_id:
            query = query.where(RedirectionItem.group_id == group_id)
        if status:
            query = query.where(RedirectionItem.status == status)

        query = query.order_by(RedirectionItem.position).offset(offset).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": item.id,
                "url": item.url,
                "match_url": item.match_url,
                "action_type": item.action_type,
                "action_code": item.action_code,
                "action_data": item.action_data,
                "match_type": item.match_type,
                "regex": item.regex == 1,
                "status": item.status,
                "title": item.title,
                "last_access": item.last_access,
                "last_count": item.last_count,
                "group_id": item.group_id
            }
            for item in result
        ]

    async def create_redirect(
        self,
        from_url: str,
        to_url: str,
        redirect_type: int = 301,
        group_id: int = 1,
        title: Optional[str] = None
    ) -> dict:
        """Create a new redirect."""
        # Get max position
        max_pos = self.session.exec(
            select(func.max(RedirectionItem.position))
        ).one() or 0

        redirect = RedirectionItem(
            url=from_url,
            match_url=from_url,
            action_type="url",
            action_code=redirect_type,
            action_data=to_url,
            match_type="url",
            regex=0,
            status="enabled",
            title=title or "",
            position=max_pos + 1,
            group_id=group_id
        )

        self.session.add(redirect)
        self.session.commit()
        self.session.refresh(redirect)

        return {
            "id": redirect.id,
            "from_url": from_url,
            "to_url": to_url,
            "type": redirect_type,
            "created": True
        }

    async def update_redirect(
        self,
        redirect_id: int,
        from_url: Optional[str] = None,
        to_url: Optional[str] = None,
        redirect_type: Optional[int] = None,
        status: Optional[str] = None
    ) -> Optional[dict]:
        """Update an existing redirect."""
        redirect = self.session.get(RedirectionItem, redirect_id)
        if not redirect:
            return None

        if from_url:
            redirect.url = from_url
            redirect.match_url = from_url
        if to_url:
            redirect.action_data = to_url
        if redirect_type:
            redirect.action_code = redirect_type
        if status:
            redirect.status = status

        self.session.add(redirect)
        self.session.commit()
        self.session.refresh(redirect)

        return {
            "id": redirect.id,
            "from_url": redirect.url,
            "to_url": redirect.action_data,
            "type": redirect.action_code,
            "status": redirect.status
        }

    async def delete_redirect(self, redirect_id: int) -> bool:
        """Delete a redirect."""
        redirect = self.session.get(RedirectionItem, redirect_id)
        if redirect:
            self.session.delete(redirect)
            self.session.commit()
            return True
        return False

    # =========================================================================
    # 404 Errors
    # =========================================================================

    async def get_404_errors(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """Get 404 error log."""
        query = select(Redirection404).order_by(
            desc(Redirection404.created)
        ).offset(offset).limit(limit)

        result = self.session.exec(query).all()

        return [
            {
                "id": error.id,
                "url": error.url,
                "domain": error.domain,
                "agent": error.agent,
                "referrer": error.referrer,
                "ip": error.ip,
                "http_code": error.http_code,
                "method": error.request_method,
                "created": error.created
            }
            for error in result
        ]

    async def get_redirect_logs(
        self,
        redirect_id: Optional[int] = None,
        limit: int = 100
    ) -> List[dict]:
        """Get redirect access logs."""
        query = select(RedirectionLog)

        if redirect_id:
            query = query.where(RedirectionLog.redirection_id == redirect_id)

        query = query.order_by(desc(RedirectionLog.created)).limit(limit)
        result = self.session.exec(query).all()

        return [
            {
                "id": log.id,
                "url": log.url,
                "sent_to": log.sent_to,
                "agent": log.agent,
                "referrer": log.referrer,
                "ip": log.ip,
                "http_code": log.http_code,
                "redirect_by": log.redirect_by,
                "created": log.created
            }
            for log in result
        ]

    # =========================================================================
    # SEO Statistics
    # =========================================================================

    async def get_seo_stats(self) -> dict:
        """Get SEO statistics dashboard."""
        # Total indexables
        total_indexables = self.session.exec(
            select(func.count()).select_from(YoastIndexable)
        ).one()

        # Posts with focus keyword
        with_keyword = self.session.exec(
            select(func.count()).select_from(YoastIndexable)
            .where(YoastIndexable.primary_focus_keyword != None)
            .where(YoastIndexable.primary_focus_keyword != "")
        ).one()

        # Cornerstone content
        cornerstone = self.session.exec(
            select(func.count()).select_from(YoastIndexable)
            .where(YoastIndexable.is_cornerstone == 1)
        ).one()

        # Active redirects
        active_redirects = self.session.exec(
            select(func.count()).select_from(RedirectionItem)
            .where(RedirectionItem.status == "enabled")
        ).one()

        # 404 errors (last 7 days)
        week_ago = datetime.now().replace(hour=0, minute=0, second=0)
        errors_7d = self.session.exec(
            select(func.count()).select_from(Redirection404)
            .where(Redirection404.created > week_ago)
        ).one()

        return {
            "total_indexables": total_indexables,
            "with_focus_keyword": with_keyword,
            "cornerstone_content": cornerstone,
            "active_redirects": active_redirects,
            "errors_7_days": errors_7d,
            "last_updated": datetime.now().isoformat()
        }

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _indexable_to_dict(self, idx: YoastIndexable) -> dict:
        """Convert indexable to dictionary."""
        return {
            "id": idx.id,
            "object_id": idx.object_id,
            "object_type": idx.object_type,
            "object_sub_type": idx.object_sub_type,
            "permalink": idx.permalink,
            "title": idx.title,
            "description": idx.description,
            "breadcrumb_title": idx.breadcrumb_title,
            "canonical": idx.canonical,
            "primary_focus_keyword": idx.primary_focus_keyword,
            "primary_focus_keyword_score": idx.primary_focus_keyword_score,
            "readability_score": idx.readability_score,
            "is_cornerstone": idx.is_cornerstone == 1,
            "is_public": idx.is_public == 1,
            "is_robots_noindex": idx.is_robots_noindex == 1,
            "open_graph": {
                "title": idx.open_graph_title,
                "description": idx.open_graph_description,
                "image": idx.open_graph_image
            },
            "twitter": {
                "title": idx.twitter_title,
                "description": idx.twitter_description,
                "image": idx.twitter_image
            },
            "link_count": idx.link_count,
            "incoming_link_count": idx.incoming_link_count,
            "estimated_reading_time": idx.estimated_reading_time_minutes,
            "created_at": idx.created_at,
            "updated_at": idx.updated_at
        }
