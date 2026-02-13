from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.model.wordpress.swpm import SWPMMember
from app.schema.wordpress.member import SWPMMemberCreate, SWPMMemberUpdate

class SWPMMemberRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, member_id: int) -> Optional[SWPMMember]:
        result = await self.session.exec(select(SWPMMember).where(SWPMMember.member_id == member_id))
        return result.first()

    async def get_by_email(self, email: str) -> Optional[SWPMMember]:
        result = await self.session.exec(select(SWPMMember).where(SWPMMember.email == email))
        return result.first()

    async def create(self, member_data: SWPMMemberCreate) -> SWPMMember:
        db_member = SWPMMember.model_validate(member_data)
        self.session.add(db_member)
        await self.session.commit()
        await self.session.refresh(db_member)
        return db_member

    async def update(self, member: SWPMMember, member_data: SWPMMemberUpdate) -> SWPMMember:
        update_data = member_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(member, key, value)
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)
        return member
