# from pydantic import BaseModel
from sqlalchemy import *
from database.database import Base
from datetime import datetime , timezone

class User_model(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), index=True)
    password = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime,default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime,default=datetime.now(tz=timezone.utc))
    is_verified = Column(Boolean,default=False)
    is_deleted = Column(Boolean,default=False)

class OTP_model(Base):
    __tablename__ = "otp"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id',ondelete='cascade'),unique=False)
    
    otp_code = Column(Integer)
    expire_at = Column(DateTime, nullable=False)
    # email = Column(String(255), unique=True, index=True)
    #mobile  = Column(Integer)
