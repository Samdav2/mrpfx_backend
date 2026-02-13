import asyncio
import sys
from unittest.mock import MagicMock

# Add app to path
sys.path.append(".")

async def verify_imports():
    print("Verifying imports...")
    try:
        from app.repo.wordpress.media import WPMediaRepository
        from app.v1.api.wordpress.media import router as media_router
        print("✅ Media module imported")

        from app.repo.wordpress.links import WPLinkRepository
        # Links API is in posts router
        from app.v1.api.wordpress.posts import router as posts_router
        print("✅ Links module imported")

        from app.repo.wordpress.posts import WPPostRepository
        # Check if new methods exist
        repo = WPPostRepository(MagicMock())
        if not hasattr(repo, "set_featured_image"):
            print("❌ WPPostRepository.set_featured_image missing")
        else:
            print("✅ WPPostRepository.set_featured_image exists")

        from app.repo.wordpress.woocommerce import WCProductRepository
        wc_repo = WCProductRepository(MagicMock())
        if not hasattr(wc_repo, "get_product_images"):
            print("❌ WCProductRepository.get_product_images missing")
        else:
            print("✅ WCProductRepository.get_product_images exists")

        from app.repo.wordpress.user import WPUserRepository
        user_repo = WPUserRepository(MagicMock())
        if not hasattr(user_repo, "delete"):
             print("❌ WPUserRepository.delete missing")
        else:
             print("✅ WPUserRepository.delete exists")

        from app.repo.wordpress.learnpress import LPCourseRepository
        lp_repo = LPCourseRepository(MagicMock())
        if not hasattr(lp_repo, "set_course_thumbnail"):
            print("❌ LPCourseRepository.set_course_thumbnail missing")
        else:
            print("✅ LPCourseRepository.set_course_thumbnail exists")

        print("\nAll checks passed!")
    except Exception as e:
        print(f"\n❌ verification failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(verify_imports())
