from sqlalchemy import create_engine

from src.models import Base
from src.config import DATABASE_URL
from sqlalchemy.orm import sessionmaker


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)



def get_db():
    """
    Get SQLAlchemy database session
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

def init_db():
    Base.metadata.create_all(engine)
    print("Success: Created the DB engine.")


