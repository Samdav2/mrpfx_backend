"""
Forms API endpoints.
Exposes WPForms and Elementor form submissions.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from pydantic import BaseModel

from app.db.session import get_session
from app.repo.wordpress.forms import FormsRepository

router = APIRouter()


# =============================================================================
# Request/Response Models
# =============================================================================

class MarkReadRequest(BaseModel):
    is_read: bool = True


# =============================================================================
# WPForms
# =============================================================================

@router.get("/wpforms/logs", tags=["Forms - WPForms"])
async def get_wpforms_logs(
    form_id: Optional[int] = None,
    log_type: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get WPForms activity logs."""
    repo = FormsRepository(session)
    return await repo.get_wpforms_logs(
        form_id=form_id,
        log_type=log_type,
        limit=limit,
        offset=offset
    )


@router.get("/wpforms/payments", tags=["Forms - WPForms"])
async def get_wpforms_payments(
    form_id: Optional[int] = None,
    status: Optional[str] = None,
    gateway: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get WPForms payment submissions."""
    repo = FormsRepository(session)
    return await repo.get_wpforms_payments(
        form_id=form_id,
        status=status,
        gateway=gateway,
        limit=limit,
        offset=offset
    )


@router.get("/wpforms/payments/{payment_id}", tags=["Forms - WPForms"])
async def get_wpforms_payment(
    payment_id: int,
    session: Session = Depends(get_session)
):
    """Get a single WPForms payment."""
    repo = FormsRepository(session)
    result = await repo.get_wpforms_payment(payment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Payment not found")
    return result


@router.get("/wpforms/payments/stats", tags=["Forms - WPForms"])
async def get_wpforms_payment_stats(
    form_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    """Get WPForms payment statistics."""
    repo = FormsRepository(session)
    return await repo.get_payment_stats(form_id=form_id)


# =============================================================================
# Elementor Forms
# =============================================================================

@router.get("/elementor/submissions", tags=["Forms - Elementor"])
async def get_elementor_submissions(
    form_name: Optional[str] = None,
    post_id: Optional[int] = None,
    status: Optional[str] = None,
    is_read: Optional[bool] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get Elementor form submissions."""
    repo = FormsRepository(session)
    return await repo.get_elementor_submissions(
        form_name=form_name,
        post_id=post_id,
        status=status,
        is_read=is_read,
        limit=limit,
        offset=offset
    )


@router.get("/elementor/submissions/{submission_id}", tags=["Forms - Elementor"])
async def get_elementor_submission(
    submission_id: int,
    session: Session = Depends(get_session)
):
    """Get a single Elementor form submission."""
    repo = FormsRepository(session)
    result = await repo.get_elementor_submission(submission_id)
    if not result:
        raise HTTPException(status_code=404, detail="Submission not found")
    return result


@router.patch("/elementor/submissions/{submission_id}/read", tags=["Forms - Elementor"])
async def mark_submission_read(
    submission_id: int,
    request: MarkReadRequest,
    session: Session = Depends(get_session)
):
    """Mark Elementor submission as read/unread."""
    repo = FormsRepository(session)
    success = await repo.mark_submission_read(submission_id, request.is_read)
    if not success:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {"success": True, "is_read": request.is_read}


@router.get("/elementor/forms", tags=["Forms - Elementor"])
async def get_elementor_form_names(
    session: Session = Depends(get_session)
):
    """Get list of unique Elementor form names with submission counts."""
    repo = FormsRepository(session)
    return await repo.get_elementor_form_names()


# =============================================================================
# Forms Statistics
# =============================================================================

@router.get("/stats", tags=["Forms - Dashboard"])
async def get_forms_stats(
    session: Session = Depends(get_session)
):
    """Get overall forms statistics."""
    repo = FormsRepository(session)
    return await repo.get_forms_stats()
