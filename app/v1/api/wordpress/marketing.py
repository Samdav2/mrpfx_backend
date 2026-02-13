"""
Marketing API endpoints.
Exposes Hustle popups and OptinPanda lead generation data.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.db.session import get_session
from app.repo.wordpress.marketing import MarketingRepository
from app.repo.wordpress.forms import FormsRepository
from app.schema.wordpress.plugins import NewsletterSubscribe

router = APIRouter()


# =============================================================================
# Public Newsletter Subscription
# =============================================================================

@router.post("/subscribe", tags=["Marketing - Public"])
async def subscribe_newsletter(
    data: NewsletterSubscribe,
    session: Session = Depends(get_session)
):
    """Public endpoint for newsletter subscription."""
    repo = FormsRepository(session)
    return await repo.create_newsletter_log(data)


# =============================================================================
# Hustle Modules
# =============================================================================

@router.get("/modules", tags=["Marketing - Modules"])
async def get_modules(
    module_type: Optional[str] = None,
    active_only: bool = True,
    limit: int = Query(100, le=500),
    session: Session = Depends(get_session)
):
    """Get Hustle marketing modules (popups, slide-ins, embeds)."""
    repo = MarketingRepository(session)
    return await repo.get_modules(
        module_type=module_type,
        active_only=active_only,
        limit=limit
    )


@router.get("/modules/{module_id}", tags=["Marketing - Modules"])
async def get_module(
    module_id: int,
    session: Session = Depends(get_session)
):
    """Get a single Hustle module with details and stats."""
    repo = MarketingRepository(session)
    result = await repo.get_module(module_id)
    if not result:
        raise HTTPException(status_code=404, detail="Module not found")
    return result


@router.get("/modules/{module_id}/stats", tags=["Marketing - Modules"])
async def get_module_stats(
    module_id: int,
    session: Session = Depends(get_session)
):
    """Get statistics for a specific Hustle module."""
    repo = MarketingRepository(session)
    return await repo.get_module_stats(module_id)


# =============================================================================
# Hustle Entries (Form Submissions)
# =============================================================================

@router.get("/entries", tags=["Marketing - Entries"])
async def get_entries(
    module_id: Optional[int] = None,
    entry_type: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get Hustle form entries/submissions."""
    repo = MarketingRepository(session)
    return await repo.get_entries(
        module_id=module_id,
        entry_type=entry_type,
        limit=limit,
        offset=offset
    )


@router.get("/entries/{entry_id}", tags=["Marketing - Entries"])
async def get_entry(
    entry_id: int,
    session: Session = Depends(get_session)
):
    """Get a single entry with full details."""
    repo = MarketingRepository(session)
    result = await repo.get_entry(entry_id)
    if not result:
        raise HTTPException(status_code=404, detail="Entry not found")
    return result


# =============================================================================
# OptinPanda Leads
# =============================================================================

@router.get("/leads", tags=["Marketing - Leads"])
async def get_leads(
    confirmed_only: bool = False,
    limit: int = Query(100, le=500),
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get OptinPanda leads."""
    repo = MarketingRepository(session)
    return await repo.get_leads(
        confirmed_only=confirmed_only,
        limit=limit,
        offset=offset
    )


@router.get("/leads/export", tags=["Marketing - Leads"])
async def export_leads(
    confirmed_only: bool = False,
    format: str = Query("json", regex="^(json|csv)$"),
    session: Session = Depends(get_session)
):
    """Export all leads in JSON or CSV format."""
    repo = MarketingRepository(session)
    return await repo.export_leads(confirmed_only=confirmed_only, format=format)


@router.get("/leads/{lead_id}", tags=["Marketing - Leads"])
async def get_lead(
    lead_id: int,
    session: Session = Depends(get_session)
):
    """Get a single lead with full details."""
    repo = MarketingRepository(session)
    result = await repo.get_lead(lead_id)
    if not result:
        raise HTTPException(status_code=404, detail="Lead not found")
    return result


# =============================================================================
# Marketing Statistics
# =============================================================================

@router.get("/stats", tags=["Marketing - Dashboard"])
async def get_marketing_stats(
    session: Session = Depends(get_session)
):
    """Get overall marketing statistics."""
    repo = MarketingRepository(session)
    return await repo.get_marketing_stats()


@router.get("/conversions", tags=["Marketing - Analytics"])
async def get_conversion_stats(
    module_id: Optional[int] = None,
    days: int = Query(30, le=365),
    session: Session = Depends(get_session)
):
    """Get daily conversion statistics."""
    repo = MarketingRepository(session)
    return await repo.get_conversion_stats(module_id=module_id, days=days)
