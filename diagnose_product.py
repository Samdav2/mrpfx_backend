"""
Diagnostic script to inspect how WooCommerce stores product data in the real database.
Run on the live server to see exactly what's in the DB for a specific product.

Usage: python diagnose_product.py <product_id>
"""
import asyncio
import sys
import os

# Add project root to path - works from project root or scripts/ subdirectory
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
# If in a subdirectory like scripts/, also add parent
sys.path.insert(0, os.path.dirname(script_dir))

from app.db.session import get_session
from sqlmodel import select
from app.model.wordpress.core import (
    WPPost, WPPostMeta, WPTerm, WPTermTaxonomy, WPTermRelationship
)


async def diagnose(product_id: int):
    async for session in get_session():
        print(f"\n{'='*60}")
        print(f"DIAGNOSING PRODUCT ID: {product_id}")
        print(f"{'='*60}")

        # 1. Check wp_posts for the product
        print(f"\n--- 1. wp_posts entry ---")
        stmt = select(WPPost).where(WPPost.ID == product_id)
        result = await session.exec(stmt)
        post = result.first()
        if post:
            print(f"  ID: {post.ID}")
            print(f"  post_title: {post.post_title}")
            print(f"  post_type: {post.post_type}")
            print(f"  post_status: {post.post_status}")
            print(f"  post_parent: {post.post_parent}")
        else:
            print(f"  NOT FOUND in wp_posts!")
            return

        # 2. Check product type via taxonomy
        print(f"\n--- 2. Product Type (via taxonomy) ---")
        type_stmt = (
            select(WPTerm, WPTermTaxonomy)
            .join(WPTermTaxonomy, WPTerm.term_id == WPTermTaxonomy.term_id)
            .join(WPTermRelationship, WPTermTaxonomy.term_taxonomy_id == WPTermRelationship.term_taxonomy_id)
            .where(
                WPTermRelationship.object_id == product_id,
                WPTermTaxonomy.taxonomy == "product_type"
            )
        )
        result = await session.exec(type_stmt)
        terms = result.all()
        if terms:
            for term, tax in terms:
                print(f"  term_id: {term.term_id}, name: '{term.name}', slug: '{term.slug}'")
                print(f"  taxonomy: '{tax.taxonomy}', term_taxonomy_id: {tax.term_taxonomy_id}")
        else:
            print(f"  NO product_type taxonomy term found!")
            # Check what taxonomies ARE linked
            print(f"\n  Checking ALL taxonomies linked to this product:")
            all_tax_stmt = (
                select(WPTerm, WPTermTaxonomy)
                .join(WPTermTaxonomy, WPTerm.term_id == WPTermTaxonomy.term_id)
                .join(WPTermRelationship, WPTermTaxonomy.term_taxonomy_id == WPTermRelationship.term_taxonomy_id)
                .where(WPTermRelationship.object_id == product_id)
            )
            result = await session.exec(all_tax_stmt)
            all_terms = result.all()
            if all_terms:
                for term, tax in all_terms:
                    print(f"    taxonomy: '{tax.taxonomy}', term: '{term.name}' (slug: '{term.slug}')")
            else:
                print(f"    NO taxonomies at all!")

        # 3. Check term_relationships directly
        print(f"\n--- 3. Raw term_relationships ---")
        rel_stmt = select(WPTermRelationship).where(WPTermRelationship.object_id == product_id)
        result = await session.exec(rel_stmt)
        rels = result.all()
        if rels:
            for r in rels:
                print(f"  object_id: {r.object_id}, term_taxonomy_id: {r.term_taxonomy_id}")
        else:
            print(f"  NO term_relationships found!")

        # 4. Check for variations (child posts)
        print(f"\n--- 4. Variations (child posts) ---")
        var_stmt = select(WPPost).where(
            WPPost.post_parent == product_id,
            WPPost.post_type == "product_variation"
        )
        result = await session.exec(var_stmt)
        variations = result.all()
        if variations:
            for v in variations:
                print(f"  Variation ID: {v.ID}, status: {v.post_status}, title: {v.post_title}")
        else:
            print(f"  NO product_variation children found!")
            # Check ALL children
            all_children_stmt = select(WPPost).where(WPPost.post_parent == product_id)
            result = await session.exec(all_children_stmt)
            children = result.all()
            if children:
                print(f"  But found {len(children)} child posts of other types:")
                for c in children:
                    print(f"    ID: {c.ID}, post_type: '{c.post_type}', status: '{c.post_status}'")
            else:
                print(f"  NO child posts at all!")

        # 5. Check key postmeta
        print(f"\n--- 5. Key postmeta ---")
        important_keys = [
            "_product_addons", "_product_attributes", "_price", "_regular_price",
            "_sale_price", "_sku", "_manage_stock", "_stock", "_stock_status",
            "_thumbnail_id", "_product_image_gallery"
        ]
        meta_stmt = select(WPPostMeta).where(
            WPPostMeta.post_id == product_id,
            WPPostMeta.meta_key.in_(important_keys)
        )
        result = await session.exec(meta_stmt)
        metas = result.all()
        if metas:
            for m in metas:
                val = m.meta_value
                if val and len(val) > 200:
                    val = val[:200] + "... (truncated)"
                print(f"  {m.meta_key}: {val}")
        else:
            print(f"  NO matching postmeta found!")

        # 6. Check ALL postmeta keys for this product
        print(f"\n--- 6. ALL meta keys for this product ---")
        all_meta_stmt = select(WPPostMeta.meta_key).where(
            WPPostMeta.post_id == product_id
        ).distinct()
        result = await session.exec(all_meta_stmt)
        all_keys = result.all()
        if all_keys:
            print(f"  Keys: {', '.join(sorted(all_keys))}")
        else:
            print(f"  NO meta keys at all!")

        # 7. Check wc_product_meta_lookup
        print(f"\n--- 7. wc_product_meta_lookup ---")
        from app.model.wordpress.woocommerce import WCProductMetaLookup
        lookup_stmt = select(WCProductMetaLookup).where(
            WCProductMetaLookup.product_id == product_id
        )
        result = await session.exec(lookup_stmt)
        lookup = result.first()
        if lookup:
            print(f"  min_price: {lookup.min_price}, max_price: {lookup.max_price}")
            print(f"  sku: {lookup.sku}, stock_status: {lookup.stock_status}")
            print(f"  stock_qty: {lookup.stock_quantity}, onsale: {lookup.onsale}")
        else:
            print(f"  NOT in wc_product_meta_lookup!")

        # 8. List some existing products for reference
        print(f"\n--- 8. First 10 products in wp_posts ---")
        products_stmt = select(WPPost).where(
            WPPost.post_type == "product",
            WPPost.post_status == "publish"
        ).limit(10)
        result = await session.exec(products_stmt)
        products = result.all()
        if products:
            for p in products:
                print(f"  ID: {p.ID} | {p.post_title[:50]}")
        else:
            print(f"  NO published products found!")

        # 9. Check what 'product_type' terms exist
        print(f"\n--- 9. All 'product_type' terms in the DB ---")
        pt_stmt = (
            select(WPTerm, WPTermTaxonomy)
            .join(WPTermTaxonomy, WPTerm.term_id == WPTermTaxonomy.term_id)
            .where(WPTermTaxonomy.taxonomy == "product_type")
        )
        result = await session.exec(pt_stmt)
        pt_terms = result.all()
        if pt_terms:
            for t, tt in pt_terms:
                print(f"  term_id: {t.term_id}, name: '{t.name}', slug: '{t.slug}', count: {tt.count}")
        else:
            print(f"  NO product_type taxonomy terms exist!")

        print(f"\n{'='*60}")
        print("DIAGNOSIS COMPLETE")
        print(f"{'='*60}")
        break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python diagnose_product.py <product_id>")
        print("  Example: python diagnose_product.py 123")
        sys.exit(1)

    pid = int(sys.argv[1])
    asyncio.run(diagnose(pid))
