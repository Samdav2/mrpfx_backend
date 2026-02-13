import asyncio
import os
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.repo.wordpress.media import WPMediaRepository
from app.model.wordpress.core import WPPost, WPPostMeta

async def verify_image_resizing():
    async with AsyncSession(engine) as session:
        repo = WPMediaRepository(session)

        # We'll use an existing image but "re-upload" it into the DB
        filename = "webuiux.jpg"
        source_rel = f"2026/02/{filename}"
        source_abs = os.path.join("wp-content/uploads", source_rel)

        if not os.path.exists(source_abs):
            print(f"Error: {source_abs} not found. Please ensure a sample image exists.")
            return

        print(f"Testing with image: {source_abs}")

        # Create attachment (this should trigger resizing)
        attachment = await repo.create_attachment(
            user_id=1,
            filename=filename,
            mime_type="image/jpeg",
            guid=f"http://localhost:8000/wp-content/uploads/{source_rel}",
            title="Resizing Test",
            alt_text="Test Alt Text"
        )

        print(f"Attachment created with ID: {attachment['id']}")

        # Verify resized files exist
        file_dir = os.path.dirname(source_abs)
        file_base, file_ext = os.path.splitext(filename)

        print("Checking for resized files:")
        for size_name, url in attachment['sizes'].items():
            if size_name == 'full': continue

            resized_filename = os.path.basename(url)
            resized_path = os.path.join(file_dir, resized_filename)

            if os.path.exists(resized_path):
                print(f"  [OK] {size_name}: {resized_path}")
            else:
                print(f"  [ERROR] {size_name} MISSING: {resized_path}")

        # Verify metadata in DB
        stmt = select(WPPostMeta).where(
            WPPostMeta.post_id == attachment['id'],
            WPPostMeta.meta_key == "_wp_attachment_metadata"
        )
        result = await session.exec(stmt)
        meta = result.first()

        if meta and meta.meta_value:
            print(f"Metadata found in DB: {meta.meta_value[:100]}...")
        else:
            print("ERROR: Metadata NOT found in DB.")

        # Cleanup: we keep the files but we could delete the DB record if we wanted.
        # For now, let's keep it for manual inspection if needed.

if __name__ == "__main__":
    asyncio.run(verify_image_resizing())
