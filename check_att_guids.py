import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPost

async def check_attachment_guids():
    async with AsyncSession(engine) as session:
        stmt = select(WPPost).where(WPPost.post_type == "attachment")
        result = await session.exec(stmt)
        atts = result.all()

        print("Attachment Guids:")
        for att in atts:
            print(f"ID: {att.ID}, Title: {att.post_title}, Guid: '{att.guid}'")

if __name__ == "__main__":
    asyncio.run(check_attachment_guids())
