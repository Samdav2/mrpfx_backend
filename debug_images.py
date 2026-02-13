import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPost, WPPostMeta

async def debug_images():
    async with AsyncSession(engine) as session:
        # Check for any _thumbnail_id in meta
        stmt = select(WPPostMeta).where(WPPostMeta.meta_key == "_thumbnail_id")
        result = await session.exec(stmt)
        metas = result.all()

        print(f"Found {len(metas)} _thumbnail_id meta entries.")
        for meta in metas:
            print(f"Post ID: {meta.post_id}, Attachment ID: {meta.meta_value}")

            # Check attachment
            try:
                att_id = int(meta.meta_value)
                att_stmt = select(WPPost).where(WPPost.ID == att_id)
                att_res = await session.exec(att_stmt)
                attachment = att_res.first()
                if attachment:
                    print(f"  Attachment found: {attachment.post_title}, Type: {attachment.post_type}, Status: {attachment.post_status}")
                    print(f"  GUID: {attachment.guid}")
                else:
                    print(f"  NO attachment found for ID {att_id}")
            except ValueError:
                print(f"  Invalid attachment ID: {meta.meta_value}")

if __name__ == "__main__":
    asyncio.run(debug_images())
