from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.model.user import User
from app.repo.wordpress.forms import FormsRepository
from app.schema.wordpress.plugins import WPFormCreate, WPFormRead, WPFormsLogRead

router = APIRouter()

@router.post("", response_model=WPFormRead)
async def create_form(
    data: WPFormCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new form (wpforms post type)"""
    repo = FormsRepository(session)
    return await repo.create_form(data, user_id=current_user.ID)

@router.get("", response_model=List[WPFormRead])
async def list_forms(
    limit: int = Query(50, le=200),
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all available forms"""
    repo = FormsRepository(session)
    return await repo.get_forms(limit=limit, offset=offset)

@router.get("/{form_id}/entries", response_model=List[WPFormsLogRead])
async def list_form_entries(
    form_id: int,
    limit: int = Query(50, le=200),
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all entries (submissions) for a specific form"""
    repo = FormsRepository(session)
    return await repo.get_wpforms_logs(form_id=form_id, limit=limit, offset=offset)

@router.get("/entries/{entry_id}", response_model=WPFormsLogRead)
async def get_form_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a single form submission entry by ID"""
    repo = FormsRepository(session)
    log = await repo.get_wpforms_log(entry_id)
    if not log:
        raise HTTPException(status_code=404, detail="Form entry not found")
    return log
