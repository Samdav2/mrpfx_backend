import sqlalchemy as sa
from app.db.session import engine
from app.model.wordpress.core import WPPost

def main():
    with sa.orm.Session(engine) as session:
        stmt = sa.select(WPPost.post_type, sa.func.count(WPPost.ID)).group_by(WPPost.post_type)
        rows = session.execute(stmt).all()
        for row in rows:
            print(f"Post Type: {row[0]}, Count: {row[1]}")

if __name__ == "__main__":
    main()
