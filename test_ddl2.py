from sqlalchemy.schema import CreateTable
from app.model.wordpress.core import WPUser
from app.db.session import wp_engine

def print_ddl():
    print(CreateTable(WPUser.__table__).compile(wp_engine.engine))

if __name__ == "__main__":
    print_ddl()
