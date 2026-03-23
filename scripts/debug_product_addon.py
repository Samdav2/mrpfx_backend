"""
Find WCPA (Acowebs) form posts and their editor data.
"""
import pymysql

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "propfirmsol_samdav"
DB_PASSWORD = "Encrypted103"
DB_NAME = "propfirmsol_WP07W"
PREFIX = "8jH_"

def main():
    conn = pymysql.connect(
        host=DB_HOST, port=DB_PORT,
        user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, charset="utf8mb4"
    )
    cursor = conn.cursor()

    # 1) Find ALL WCPA form posts
    print("=== WCPA Form Posts ===")
    cursor.execute(f"""
        SELECT ID, post_title, post_type, post_status
        FROM {PREFIX}posts
        WHERE post_type LIKE '%wcpa%'
        LIMIT 30
    """)
    forms = cursor.fetchall()
    if forms:
        for pid, title, ptype, status in forms:
            print(f"\n  ID={pid}, title={title}, type={ptype}, status={status}")
            cursor.execute(
                f"SELECT meta_key, LEFT(meta_value, 500) FROM {PREFIX}postmeta WHERE post_id = %s",
                (pid,)
            )
            for mk, mv in cursor.fetchall():
                print(f"    {mk}: {mv}")
    else:
        print("  (none found)")

    # 2) Check WCPA options table for global settings
    print("\n=== WCPA Options ===")
    cursor.execute(f"""
        SELECT option_name, LEFT(option_value, 500)
        FROM {PREFIX}options
        WHERE option_name LIKE '%wcpa%'
        ORDER BY option_name
    """)
    for name, val in cursor.fetchall():
        print(f"  {name}: {val}")

    # 3) Check products that DO have _wcpa_product_meta with actual data
    print("\n=== Products with non-empty WCPA meta ===")
    cursor.execute(f"""
        SELECT post_id, LEFT(meta_value, 500)
        FROM {PREFIX}postmeta
        WHERE meta_key = '_wcpa_product_meta'
          AND meta_value != 'a:0:{{}}'
          AND meta_value != ''
        LIMIT 10
    """)
    rows = cursor.fetchall()
    if rows:
        for pid, val in rows:
            cursor.execute(f"SELECT post_title FROM {PREFIX}posts WHERE ID = %s", (pid,))
            title = cursor.fetchone()
            print(f"  Product {pid} ({title[0] if title else 'unknown'}): {val}")
    else:
        print("  (none found)")

    # 4) Check _wcpa_fb-editor-data entries
    print("\n=== WCPA Editor Data entries ===")
    cursor.execute(f"""
        SELECT pm.post_id, p.post_title, LEFT(pm.meta_value, 500)
        FROM {PREFIX}postmeta pm
        JOIN {PREFIX}posts p ON p.ID = pm.post_id
        WHERE pm.meta_key = '_wcpa_fb-editor-data'
        LIMIT 10
    """)
    rows = cursor.fetchall()
    if rows:
        for pid, title, val in rows:
            print(f"  Post {pid} ({title}): {val}")
    else:
        print("  (none found)")

    cursor.close()
    conn.close()
    print("\nDone!")

if __name__ == "__main__":
    main()
