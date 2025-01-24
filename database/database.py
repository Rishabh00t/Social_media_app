from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()

# Ensure database tables are created
Base.metadata.create_all(bind=engine)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
