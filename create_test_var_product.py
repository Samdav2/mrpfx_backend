import asyncio
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from decimal import Decimal
from app.db.session import get_session
from app.repo.wordpress.woocommerce import WCProductRepository
from app.schema.wordpress.woocommerce import (
    WCProductCreate, WCProductVariationCreate, WCProductAddonField
)

async def main():
    try:
        async for session in get_session():
            repo = WCProductRepository(session)
            print("Creating test variable product...")

            base_product = WCProductCreate(
                name="Frontend Test - Variable Product",
                description="Product with variations and addons for frontend testing.",
                short_description="Test product.",
                status="publish",
                type="variable",
                manage_stock=False,
                attributes=[
                    {
                        "name": "Access Duration",
                        "options": ["1 Month", "Lifetime"],
                        "visible": True,
                        "variation": True,
                        "position": 0
                    }
                ],
                addons=[
                    WCProductAddonField(
                        name="Telegram Username",
                        type="text",
                        required=True,
                        description="Enter your Telegram handle below.",
                        position=0
                    )
                ]
            )

            product = await repo.create_product(base_product)
            print(f"Created Parent Product ID: {product.id}")

            var1 = WCProductVariationCreate(
                regular_price=Decimal("49.99"),
                manage_stock=False,
                stock_status="instock",
                attributes=[{"name": "Access Duration", "option": "1 Month"}],
                description="One month access.",
                status="publish"
            )
            v1_obj = await repo.create_variation(product.id, var1)
            print(f"Created Variation 1 (1 Month) ID: {v1_obj.id if v1_obj else 'Failed'}")

            var2 = WCProductVariationCreate(
                regular_price=Decimal("299.99"),
                sale_price=Decimal("249.99"),
                manage_stock=False,
                stock_status="instock",
                attributes=[{"name": "Access Duration", "option": "Lifetime"}],
                description="Lifetime access on sale.",
                status="publish"
            )
            v2_obj = await repo.create_variation(product.id, var2)
            print(f"Created Variation 2 (Lifetime) ID: {v2_obj.id if v2_obj else 'Failed'}")

            print(f"\nSuccessfully created test product. Product ID: {product.id}")
            break
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
