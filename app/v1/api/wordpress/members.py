from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.repo.wordpress.member import SWPMMemberRepository
from app.schema.wordpress.member import SWPMMemberRead, SWPMMemberCreate, SWPMMemberUpdate

router = APIRouter()

@router.get("/{member_id}", response_model=SWPMMemberRead)
async def get_member(
    member_id: int,
    session: AsyncSession = Depends(get_session)
):
    repo = SWPMMemberRepository(session)
    member = await repo.get_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@router.post("/", response_model=SWPMMemberRead)
async def create_member(
    member_data: SWPMMemberCreate,
    session: AsyncSession = Depends(get_session)
):
    repo = SWPMMemberRepository(session)
    existing = await repo.get_by_email(member_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Member email already exists")
    return await repo.create(member_data)

@router.put("/{member_id}", response_model=SWPMMemberRead)
async def update_member(
    member_id: int,
    member_data: SWPMMemberUpdate,
    session: AsyncSession = Depends(get_session)
):
    repo = SWPMMemberRepository(session)
    member = await repo.get_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return await repo.update(member, member_data)
