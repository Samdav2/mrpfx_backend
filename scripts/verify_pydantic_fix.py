import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.repo.wordpress.posts import WPPostRepository

async def verify_featured_image_output():
    async with AsyncSession(engine) as session:
        repo = WPPostRepository(session)

        # Check for a post that has a featured image (e.g. 41)
        post_id = 41
        featured_image = await repo.get_featured_image(post_id)

        if featured_image:
            print(f"Featured image for post {post_id}:")
            for key, value in featured_image.items():
                print(f"  {key}: {value}")

            # Check for extra fields that were causing warnings
            forbidden_keys = ["mime_type", "date_created"]
            for key in forbidden_keys:
                if key in featured_image:
                    print(f"  [ERROR] Forbidden key still present: {key}")
                else:
                    print(f"  [OK] Key {key} is absent.")
        else:
            print(f"No featured image found for post {post_id} or post not found.")

if __name__ == "__main__":
    asyncio.run(verify_featured_image_output())
