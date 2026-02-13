"""
SEO API endpoints.
Exposes Yoast SEO and Redirection plugin data.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from pydantic import BaseModel

from app.db.session import get_session
from app.repo.wordpress.seo import SEORepository

router = APIRouter()


# =============================================================================
# Request/Response Models
# =============================================================================

class UpdateSEORequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    focus_keyword: Optional[str] = None
    is_cornerstone: Optional[bool] = None
    canonical: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    twitter_title: Optional[str] = None
    twitter_description: Optional[str] = None


class CreateRedirectRequest(BaseModel):
    from_url: str
    to_url: str
    redirect_type: int = 301  # 301, 302, 307, 308
    group_id: int = 1
    title: Optional[str] = None


class UpdateRedirectRequest(BaseModel):
    from_url: Optional[str] = None
    to_url: Optional[str] = None
    redirect_type: Optional[int] = None
    status: Optional[str] = None  # "enabled", "disabled"


# =============================================================================
# Yoast SEO - Indexables
# =============================================================================

@router.get("/indexables", tags=["SEO - Yoast"])
async def get_indexables(
    object_type: Optional[str] = None,
    object_sub_type: Optional[str] = None,
    is_public: bool = True,
    limit: int = Query(100, le=500),
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get Yoast SEO indexables."""
    repo = SEORepository(session)
    return await repo.get_indexables(
        object_type=object_type,
        object_sub_type=object_sub_type,
        is_public=is_public,
        limit=limit,
        offset=offset
    )


@router.get("/posts/{post_id}", tags=["SEO - Yoast"])
async def get_post_seo(
    post_id: int,
    session: Session = Depends(get_session)
):
    """Get SEO data for a specific post."""
    repo = SEORepository(session)
    result = await repo.get_post_seo(post_id)
    if not result:
        raise HTTPException(status_code=404, detail="SEO data not found for this post")
    return result


@router.put("/posts/{post_id}", tags=["SEO - Yoast"])
async def update_post_seo(
    post_id: int,
    request: UpdateSEORequest,
    session: Session = Depends(get_session)
):
    """Update SEO metadata for a post."""
    repo = SEORepository(session)
    result = await repo.update_post_seo(
        post_id=post_id,
        title=request.title,
        description=request.description,
        focus_keyword=request.focus_keyword,
        is_cornerstone=request.is_cornerstone,
        canonical=request.canonical,
        og_title=request.og_title,
        og_description=request.og_description,
        og_image=request.og_image,
        twitter_title=request.twitter_title,
        twitter_description=request.twitter_description
    )
    if not result:
        raise HTTPException(status_code=404, detail="SEO data not found for this post")
    return result


@router.get("/links", tags=["SEO - Yoast"])
async def get_seo_links(
    post_id: Optional[int] = None,
    link_type: Optional[str] = None,
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get SEO internal/external links."""
    repo = SEORepository(session)
    return await repo.get_seo_links(post_id=post_id, link_type=link_type, limit=limit)


# =============================================================================
# Redirection Plugin
# =============================================================================

@router.get("/redirects/groups", tags=["SEO - Redirects"])
async def get_redirect_groups(
    session: Session = Depends(get_session)
):
    """Get redirect groups."""
    repo = SEORepository(session)
    return await repo.get_redirect_groups()


@router.get("/redirects", tags=["SEO - Redirects"])
async def get_redirects(
    group_id: Optional[int] = None,
    status: str = "enabled",
    limit: int = Query(100, le=500),
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get redirect items."""
    repo = SEORepository(session)
    return await repo.get_redirects(
        group_id=group_id,
        status=status,
        limit=limit,
        offset=offset
    )


@router.post("/redirects", tags=["SEO - Redirects"])
async def create_redirect(
    request: CreateRedirectRequest,
    session: Session = Depends(get_session)
):
    """Create a new redirect."""
    repo = SEORepository(session)
    return await repo.create_redirect(
        from_url=request.from_url,
        to_url=request.to_url,
        redirect_type=request.redirect_type,
        group_id=request.group_id,
        title=request.title
    )


@router.put("/redirects/{redirect_id}", tags=["SEO - Redirects"])
async def update_redirect(
    redirect_id: int,
    request: UpdateRedirectRequest,
    session: Session = Depends(get_session)
):
    """Update an existing redirect."""
    repo = SEORepository(session)
    result = await repo.update_redirect(
        redirect_id=redirect_id,
        from_url=request.from_url,
        to_url=request.to_url,
        redirect_type=request.redirect_type,
        status=request.status
    )
    if not result:
        raise HTTPException(status_code=404, detail="Redirect not found")
    return result


@router.delete("/redirects/{redirect_id}", tags=["SEO - Redirects"])
async def delete_redirect(
    redirect_id: int,
    session: Session = Depends(get_session)
):
    """Delete a redirect."""
    repo = SEORepository(session)
    success = await repo.delete_redirect(redirect_id)
    if not success:
        raise HTTPException(status_code=404, detail="Redirect not found")
    return {"success": True, "message": "Redirect deleted"}


@router.get("/redirects/{redirect_id}/logs", tags=["SEO - Redirects"])
async def get_redirect_logs(
    redirect_id: int,
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get redirect access logs."""
    repo = SEORepository(session)
    return await repo.get_redirect_logs(redirect_id=redirect_id, limit=limit)


# =============================================================================
# 404 Errors
# =============================================================================

@router.get("/404-errors", tags=["SEO - Errors"])
async def get_404_errors(
    limit: int = Query(100, le=500),
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get 404 error log."""
    repo = SEORepository(session)
    return await repo.get_404_errors(limit=limit, offset=offset)


# =============================================================================
# SEO Statistics
# =============================================================================

@router.get("/stats", tags=["SEO - Dashboard"])
async def get_seo_stats(
    session: Session = Depends(get_session)
):
    """Get SEO statistics dashboard."""
    repo = SEORepository(session)
    return await repo.get_seo_stats()
