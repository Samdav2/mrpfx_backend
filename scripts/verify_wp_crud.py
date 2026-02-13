import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from app.model.wordpress.core import WPUser
from app.model.wordpress.woocommerce import WCOrder
from app.model.wordpress.swpm import SWPMMember
from app.db.session import engine, ini_db
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

async def verify_models():
    print("Verifying database models...")
    await ini_db()

    async with AsyncSession(engine) as session:
        # Check Users
        print("Checking WPUser table...")
        try:
            result = await session.exec(select(WPUser).limit(1))
            user = result.first()
            print(f"WPUser check: {'Found user' if user else 'Table empty but accessible'}")
        except Exception as e:
            print(f"Error checking WPUser: {e}")

        # Check Orders
        print("Checking WCOrder table...")
        try:
            result = await session.exec(select(WCOrder).limit(1))
            order = result.first()
            print(f"WCOrder check: {'Found order' if order else 'Table empty but accessible'}")
        except Exception as e:
            print(f"Error checking WCOrder: {e}")

        # Check Members
        print("Checking SWPMMember table...")
        try:
            result = await session.exec(select(SWPMMember).limit(1))
            member = result.first()
            print(f"SWPMMember check: {'Found member' if member else 'Table empty but accessible'}")
        except Exception as e:
            print(f"Error checking SWPMMember: {e}")

        # Check LearnPress
        from app.model.wordpress.learnpress import (
            LPSection, LPSectionItem, LPQuizQuestion,
            LPQuestionAnswer, LPUserItemResult, LPOrderItem, LPReviewLog
        )

        tables_to_check = [
            (LPSection, "LPSection"),
            (LPSectionItem, "LPSectionItem"),
            (LPQuizQuestion, "LPQuizQuestion"),
            (LPQuestionAnswer, "LPQuestionAnswer"),
            (LPUserItemResult, "LPUserItemResult"),
            (LPOrderItem, "LPOrderItem"),
            (LPReviewLog, "LPReviewLog")
        ]

        for model, name in tables_to_check:
            print(f"Checking {name} table...")
            try:
                result = await session.exec(select(model).limit(1))
                item = result.first()
                print(f"{name} check: {'Found item' if item else 'Table empty but accessible'}")
            except Exception as e:
                print(f"Error checking {name}: {e}")

if __name__ == "__main__":
    asyncio.run(verify_models())
