from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.repo.wordpress.user import WPUserRepository
from app.schema.wordpress.user import WPUserRead, WPUserCreate, WPUserUpdate

router = APIRouter()

@router.get("/", response_model=List[WPUserRead])
async def get_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    repo = WPUserRepository(session)
    skip = (page - 1) * per_page
    return await repo.get_all(skip=skip, limit=per_page)

@router.get("/{user_id}", response_model=WPUserRead)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    repo = WPUserRepository(session)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=WPUserRead)
async def create_user(
    user_data: WPUserCreate,
    session: AsyncSession = Depends(get_session)
):
    repo = WPUserRepository(session)
    existing = await repo.get_by_login(user_data.user_login)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    return await repo.create(user_data)

@router.put("/{user_id}", response_model=WPUserRead)
async def update_user(
    user_id: int,
    user_data: WPUserUpdate,
    session: AsyncSession = Depends(get_session)
):
    repo = WPUserRepository(session)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await repo.update(user, user_data)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    repo = WPUserRepository(session)
    success = await repo.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.get("/{user_id}/roles", response_model=List[str])
async def get_user_roles(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    repo = WPUserRepository(session)
    # Verify user exists
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return await repo.get_roles(user_id)

@router.put("/{user_id}/roles")
async def set_user_roles(
    user_id: int,
    roles: List[str],
    session: AsyncSession = Depends(get_session)
):
    repo = WPUserRepository(session)
    # Verify user exists
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await repo.set_roles(user_id, roles)
    return {"message": "Roles updated successfully"}
