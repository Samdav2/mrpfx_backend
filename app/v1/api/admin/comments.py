from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.model.user import User
from app.repo.wordpress.posts import WPCommentRepository
from app.schema.wordpress.post import WPCommentRead, WPCommentUpdate

router = APIRouter()

@router.get("", response_model=List[WPCommentRead])
async def list_comments(
    status: str = Query("approve", description="Comment status (approve, hold, spam, trash)"),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all comments with filtering by status"""
    repo = WPCommentRepository(session)
    return await repo.get_comments(status=status, limit=limit, offset=offset)

@router.put("/{comment_id}", response_model=WPCommentRead)
async def update_comment(
    comment_id: int,
    data: WPCommentUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update comment content or moderation status"""
    repo = WPCommentRepository(session)
    comment = await repo.update_comment(comment_id, data)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    force: bool = Query(False, description="Permanently delete if True"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Move comment to trash or permanently delete"""
    repo = WPCommentRepository(session)
    success = await repo.delete_comment(comment_id, force=force)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")

    message = "Comment permanently deleted" if force else "Comment moved to trash"
    return {"status": "success", "message": message}
