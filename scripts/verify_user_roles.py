import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.repo.wordpress.user import WPUserRepository

async def verify_user_roles():
    async with AsyncSession(engine) as session:
        repo = WPUserRepository(session)

        # Test with user ID 7 (or any other existing user)
        user_id = 7
        try:
            roles = await repo.get_roles(user_id)
            print(f"Roles for user {user_id}: {roles}")

            # Test setting roles (round-trip)
            test_roles = ["administrator", "editor"]
            print(f"Setting roles to: {test_roles}")
            await repo.set_roles(user_id, test_roles)

            new_roles = await repo.get_roles(user_id)
            print(f"Verified roles: {new_roles}")

            if set(test_roles) == set(new_roles):
                print("[OK] Role round-trip success!")
            else:
                print("[ERROR] Role round-trip failed!")

        except Exception as e:
            print(f"Verification failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify_user_roles())
