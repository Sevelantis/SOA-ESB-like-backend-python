from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import src.config as config

db_engine = create_engine(url=config.DB_CONNECTION_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base = declarative_base()

def database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        