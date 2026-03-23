from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_session
from app.repo.wordpress.options import WPOptionRepository
from app.schema.admin import ForcePasswordResetUpdate, SecuritySettingsRead
from app.dependencies.auth import get_current_admin
from datetime import datetime

router = APIRouter()

@router.get("/security/force-reset", response_model=SecuritySettingsRead)
async def get_security_settings(
    session: AsyncSession = Depends(get_session),
    admin=Depends(get_current_admin)
):
    """Retrieve current force password reset settings."""
    option_repo = WPOptionRepository(session)
    force_reset_date = await option_repo.get_option("force_password_reset_date")

    return SecuritySettingsRead(
        force_password_reset_date=int(force_reset_date) if force_reset_date else None,
        last_updated=datetime.now()
    )

@router.post("/security/force-reset", response_model=SecuritySettingsRead)
async def update_security_settings(
    request: ForcePasswordResetUpdate,
    session: AsyncSession = Depends(get_session),
    admin=Depends(get_current_admin)
):
    """Update the global force password reset date."""
    option_repo = WPOptionRepository(session)

    if request.force_reset_date is not None:
        await option_repo.update_option("force_password_reset_date", str(request.force_reset_date))

    force_reset_date = await option_repo.get_option("force_password_reset_date")

    return SecuritySettingsRead(
        force_password_reset_date=int(force_reset_date) if force_reset_date else None,
        last_updated=datetime.now()
    )
