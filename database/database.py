from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
import time,os
from dotenv import load_dotenv


# def get_engine(max_retries=5):
#     for _ in range(max_retries):
#         try:
#             engine = create_engine(SQLALCHEMY_DATABASE_URL)
#             # Test connection
#             with engine.connect():
#                 return engine
#         except OperationalError as e:
#             # Log the exception (optional)
#             print(f"Database connection failed: {e}. Retrying in 5 seconds...")
#             time.sleep(5)

#     # Raise a generic Exception or SQLAlchemyError instead of OperationalError
#     raise Exception("Could not connect to database after multiple attempts")


# Create the SQLAlchemy engine

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
