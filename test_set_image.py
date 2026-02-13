import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.repo.wordpress.posts import WPPostRepository

async def test_set_image():
    async with AsyncSession(engine) as session:
        repo = WPPostRepository(session)
        # Set attachment 35 for page 41
        success = await repo.set_featured_image(41, 35)
        print(f"Set image success: {success}")
        if success:
            await session.commit()
            print("Commited.")

            # Now fetch it back
            page = await repo.get_post(41)
            if page and page.featured_image:
                print(f"Fetched image: {page.featured_image.title}")
            else:
                print("FAILED to fetch image back.")

if __name__ == "__main__":
    asyncio.run(test_set_image())
