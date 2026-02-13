"""
WordPress Links Repository.
Provides CRUD operations for WordPress links (8jH_links table).
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.model.wordpress.core import WPLink


class WPLinkRepository:
    """Repository for WordPress links"""

    def __init__(self, session: AsyncSession):
        self.session = session

    # Get list of links
    async def get_links(
        self,
        visible_only: bool = True,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get list of WordPress links"""
        query = select(WPLink)

        if visible_only:
            query = query.where(WPLink.link_visible == "Y")

        query = query.order_by(WPLink.link_rating.desc(), WPLink.link_name).offset(offset).limit(limit)
        result = await self.session.exec(query)
        links = result.all()

        return [self._link_to_dict(link) for link in links]

    # Get a single link by ID
    async def get_link(self, link_id: int) -> Optional[Dict[str, Any]]:
        """Get a single link by ID"""
        query = select(WPLink).where(WPLink.link_id == link_id)
        result = await self.session.exec(query)
        link = result.first()

        if not link:
            return None

        return self._link_to_dict(link)

    # Create a new link
    async def create_link(
        self,
        url: str,
        name: str,
        owner_id: int,
        description: str = "",
        target: str = "",
        rel: str = "",
        visible: str = "Y",
        image: str = "",
        notes: str = "",
        rss: str = ""
    ) -> Dict[str, Any]:
        """Create a new WordPress link"""
        link = WPLink(
            link_url=url,
            link_name=name,
            link_image=image,
            link_target=target,
            link_description=description,
            link_visible=visible,
            link_owner=owner_id,
            link_rating=0,
            link_updated=datetime.now(),
            link_rel=rel,
            link_notes=notes,
            link_rss=rss
        )

        self.session.add(link)
        await self.session.commit()
        await self.session.refresh(link)

        return self._link_to_dict(link)

    # Update a link
    async def update_link(
        self,
        link_id: int,
        url: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        target: Optional[str] = None,
        rel: Optional[str] = None,
        visible: Optional[str] = None,
        image: Optional[str] = None,
        notes: Optional[str] = None,
        rss: Optional[str] = None,
        rating: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Update an existing link"""
        query = select(WPLink).where(WPLink.link_id == link_id)
        result = await self.session.exec(query)
        link = result.first()

        if not link:
            return None

        if url is not None:
            link.link_url = url
        if name is not None:
            link.link_name = name
        if description is not None:
            link.link_description = description
        if target is not None:
            link.link_target = target
        if rel is not None:
            link.link_rel = rel
        if visible is not None:
            link.link_visible = visible
        if image is not None:
            link.link_image = image
        if notes is not None:
            link.link_notes = notes
        if rss is not None:
            link.link_rss = rss
        if rating is not None:
            link.link_rating = rating

        link.link_updated = datetime.now()
        self.session.add(link)
        await self.session.commit()
        await self.session.refresh(link)

        return self._link_to_dict(link)

    # Delete a link
    async def delete_link(self, link_id: int) -> bool:
        """Delete a link permanently"""
        query = select(WPLink).where(WPLink.link_id == link_id)
        result = await self.session.exec(query)
        link = result.first()

        if not link:
            return False

        await self.session.delete(link)
        await self.session.commit()
        return True

    # Helper: Convert link model to dict
    def _link_to_dict(self, link: WPLink) -> Dict[str, Any]:
        """Convert WPLink model to dictionary"""
        return {
            "id": link.link_id,
            "url": link.link_url,
            "name": link.link_name,
            "image": link.link_image,
            "target": link.link_target,
            "description": link.link_description,
            "visible": link.link_visible == "Y",
            "owner_id": link.link_owner,
            "rating": link.link_rating,
            "updated": link.link_updated,
            "rel": link.link_rel,
            "notes": link.link_notes,
            "rss": link.link_rss
        }
