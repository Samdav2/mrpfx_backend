import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPost

async def check_attachment_parents():
    async with AsyncSession(engine) as session:
        stmt = select(WPPost).where(WPPost.post_type == "attachment")
        result = await session.exec(stmt)
        attachments = result.all()

        print("Attachments and their parents:")
        for att in attachments:
            print(f"ID: {att.ID}, Title: {att.post_title}, Parent: {att.post_parent}")
            if att.post_parent > 0:
                parent = await session.get(WPPost, att.post_parent)
                if parent:
                    print(f"  Parent Title: {parent.post_title}, Type: {parent.post_type}")

if __name__ == "__main__":
    asyncio.run(check_attachment_parents())
