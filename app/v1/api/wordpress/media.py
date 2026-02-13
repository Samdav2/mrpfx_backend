"""
WordPress Media API Endpoints.
Full CRUD operations for WordPress media attachments.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Form, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel, Field

from app.db.session import get_session
from app.repo.wordpress.media import WPMediaRepository
from app.dependencies.auth import get_current_user
from app.model.user import User


router = APIRouter()


# ============== Request/Response Schemas ==============

class MediaCreate(BaseModel):
    """Schema for creating media attachment"""
    filename: str = Field(..., description="Original filename")
    mime_type: str = Field(..., description="MIME type (e.g., image/jpeg)")
    url: str = Field(..., description="Full URL to the file (guid)")
    title: Optional[str] = Field(None, description="Media title")
    description: Optional[str] = Field(None, description="Media description")
    alt_text: Optional[str] = Field(None, description="Alt text for accessibility")
    caption: Optional[str] = Field(None, description="Media caption")


class MediaUpdate(BaseModel):
    """Schema for updating media attachment"""
    title: Optional[str] = None
    description: Optional[str] = None
    alt_text: Optional[str] = None
    caption: Optional[str] = None


# ============== Endpoints ==============

@router.get("/", tags=["Media"])
@router.get("", tags=["Media"], include_in_schema=False)
async def get_media(
    mime_type: Optional[str] = Query(None, description="Filter by MIME type (e.g., 'image', 'video')"),
    search: Optional[str] = Query(None, description="Search by title"),
    limit: int = Query(20, le=100),
    offset: int = Query(0),
    session: AsyncSession = Depends(get_session)
):
    """Get list of media attachments"""
    repo = WPMediaRepository(session)
    return await repo.get_attachments(
        mime_type=mime_type,
        search=search,
        limit=limit,
        offset=offset
    )


@router.get("/{attachment_id}", tags=["Media"])
async def get_media_item(
    attachment_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get a single media attachment by ID"""
    repo = WPMediaRepository(session)
    media = await repo.get_attachment(attachment_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media


@router.post("/", tags=["Media"])
@router.post("", tags=["Media"], include_in_schema=False)
async def create_media(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    alt_text: Optional[str] = Form(None),
    caption: Optional[str] = Form(None),
    request: Request = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Upload a new media attachment.
    """
    import os
    import shutil
    from datetime import datetime

    # Create directory structure: wp-content/uploads/{year}/{month}
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    upload_dir = f"wp-content/uploads/{year}/{month}"
    os.makedirs(upload_dir, exist_ok=True)

    # Save file
    file_path = f"{upload_dir}/{file.filename}"
    # Avoid overwrite by appending timestamp if exists? Or just simple for now.

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Generate URL
    # Assuming request.base_url is correct, or use a configured base
    base_url = str(request.base_url).rstrip("/")
    file_url = f"{base_url}/{file_path}"

    repo = WPMediaRepository(session)
    return await repo.create_attachment(
        user_id=current_user.ID,
        filename=file.filename,
        mime_type=file.content_type,
        guid=file_url,
        title=title,
        description=description,
        alt_text=alt_text,
        caption=caption
    )


@router.put("/{attachment_id}", tags=["Media"])
async def update_media(
    attachment_id: int,
    media_data: MediaUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update a media attachment's metadata"""
    repo = WPMediaRepository(session)
    media = await repo.update_attachment(
        attachment_id=attachment_id,
        title=media_data.title,
        description=media_data.description,
        alt_text=media_data.alt_text,
        caption=media_data.caption
    )
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media


@router.delete("/{attachment_id}", tags=["Media"])
async def delete_media(
    attachment_id: int,
    force: bool = Query(False, description="Permanently delete instead of trashing"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a media attachment (moves to trash unless force=true)"""
    repo = WPMediaRepository(session)
    success = await repo.delete_attachment(attachment_id, force=force)
    if not success:
        raise HTTPException(status_code=404, detail="Media not found")
    return {"success": True, "message": "Media deleted" if force else "Media moved to trash"}


@router.get("/{attachment_id}/urls", tags=["Media"])
async def get_media_urls(
    attachment_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get all available size URLs for a media attachment"""
    repo = WPMediaRepository(session)
    urls = await repo.get_attachment_urls(attachment_id)
    if not urls:
        raise HTTPException(status_code=404, detail="Media not found")
    return urls
