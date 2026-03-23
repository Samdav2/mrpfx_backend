from sqlmodel import select, or_, create_engine, Session, SQLModel
from app.model.wordpress.core import WPUser as User
import os

DATABASE_URL = f"sqlite:////{os.path.abspath('/home/rehack/PycharmProjects/mrpfx-backend/mrpfx.db')}"
engine = create_engine(DATABASE_URL)

def test_get_by_email_or_login():
    with Session(engine) as session:
        # First get any user to see if it even works
        try:
            stmt = select(User).limit(1)
            result = session.exec(stmt).first()
            if result:
                print(f"Successfully retrieved user: {result.user_login}")
                print(f"Registered: [{result.user_registered}] ({type(result.user_registered)})")

                # Now try by identifier
                identifier = result.user_login
                stmt2 = select(User).where(or_(User.user_email == identifier, User.user_login == identifier))
                result2 = session.exec(stmt2).first()
                print(f"Retrieved by identifier {identifier}: {result2 is not None}")
            else:
                print("No users in database")
        except Exception as e:
            print(f"FAILED: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_get_by_email_or_login()
