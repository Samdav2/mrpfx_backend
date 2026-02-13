import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPost

async def check_att_35():
    async with AsyncSession(engine) as session:
        att = await session.get(WPPost, 35)
        if att:
            print(f"Attachment 35:")
            print(f"  Title: {att.post_title}")
            print(f"  Type: {att.post_type}")
            print(f"  Guid: {att.guid}")
            print(f"  Mime: {att.post_mime_type}")

if __name__ == "__main__":
    asyncio.run(check_att_35())
