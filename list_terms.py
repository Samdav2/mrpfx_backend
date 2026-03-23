import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPTerm, WPTermTaxonomy

async def list_terms():
    async with AsyncSession(engine) as session:
        stmt = select(WPTerm.name, WPTermTaxonomy.taxonomy).join(WPTermTaxonomy, WPTerm.term_id == WPTermTaxonomy.term_id)
        result = await session.exec(stmt)
        terms = result.all()

        print("Terms and Taxonomies:")
        for name, taxonomy in terms:
            print(f"- {name} ({taxonomy})")

if __name__ == "__main__":
    asyncio.run(list_terms())
