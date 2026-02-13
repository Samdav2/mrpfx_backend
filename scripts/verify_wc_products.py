import asyncio
import os
import sys
from decimal import Decimal

# Add project root to path
sys.path.append(os.getcwd())

from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.repo.wordpress.woocommerce import WCProductRepository
from app.schema.wordpress.woocommerce import (
    WCProductCreate, WCProductVariationCreate
)

async def verify():
    async with AsyncSession(engine) as session:
        repo = WCProductRepository(session)

        print("\n=== Final Aggregation Test ===")
        new_prod = await repo.create_product(WCProductCreate(
            name="Final Test Product",
            type="variable"
        ))

        await repo.create_variation(new_prod.id, WCProductVariationCreate(
            sku=f"FINAL-VAR-{os.urandom(1).hex()}",
            regular_price=Decimal("99.99"),
            attributes=[{"name": "Color", "option": "Gold"}]
        ))

        full_p = await repo.get_product_full(new_prod.id)
        if full_p and len(full_p.variations) > 0:
            print(f"SUCCESS: Full product '{full_p.name}' has {len(full_p.variations)} variations.")
            print(f"Variation 1 SKU: {full_p.variations[0].sku}")
        else:
            print(f"FAILED: Full product has {len(full_p.variations) if full_p else 'N/A'} variations.")

        # Cleanup
        await repo.delete_product(new_prod.id, force=True)
        print("Cleaned up.")

if __name__ == "__main__":
    asyncio.run(verify())
