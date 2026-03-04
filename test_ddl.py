from sqlalchemy.schema import CreateTable
from app.model.wordpress.woocommerce import WCSession
from app.model.wordpress.core import WPComment
from app.db.session import wp_engine

def print_ddl():
    print(CreateTable(WCSession.__table__).compile(wp_engine.engine))
    print(CreateTable(WPComment.__table__).compile(wp_engine.engine))

if __name__ == "__main__":
    print_ddl()
