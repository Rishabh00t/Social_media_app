from sqlalchemy import *
from database.database import Base
from datetime import datetime , timezone
from sqlalchemy.orm import Relationship


class Post_model(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id',ondelete='cascade'))
    user = Relationship("User_model")
    title = Column(String(255))
    captions = Column(Text,nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime,default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime,default=datetime.now(tz=timezone.utc))    
    is_deleted = Column(Boolean,default=False)
    like_count = Column(Integer, default=0)