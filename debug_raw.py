import sqlalchemy as sa
from app.db.session import engine
from app.model.wordpress.core import WPPostMeta
import phpserialize
import json

def test_parse_addon(addon_raw):
    addons = []
    try:
        addon_data = json.loads(addon_raw)
        print("Parsed as JSON")
    except Exception:
        try:
            addon_data = phpserialize.loads(addon_raw.encode(), decode_strings=True)
            print("Parsed as PHP Serialize")
            if isinstance(addon_data, dict):
                addon_data = list(addon_data.values())
        except Exception as e:
            print(f"Failed BOTH: {e}")
            return

    if not isinstance(addon_data, list):
        print(f"Not a list: {type(addon_data)}")
        return

    for i, ad in enumerate(addon_data):
        if isinstance(ad, dict):
            name = ad.get("name") or ad.get("label") or ad.get("field_name")
            print(f"Found addon: {name} (type: {ad.get('type')})")
        else:
            print(f"Skipped non-dict addon item: {type(ad)}")

def main():
    with sa.orm.Session(engine) as session:
        # Check specific product first if provided by user (e.g. 18618)
        stmt = sa.select(WPPostMeta).where(WPPostMeta.meta_key.in_(["_product_addons", "_wcpa_product_meta", "_wc_product_addons"]))
        rows = session.scalars(stmt).all()

        print(f"Found {len(rows)} addon records.")
        for row in rows[:15]:
            print("\n-------------------------")
            print(f"Post {row.post_id} Key {row.meta_key}")
            print(f"Raw: {row.meta_value[:200]}...")
            test_parse_addon(row.meta_value)

if __name__ == "__main__":
    main()
