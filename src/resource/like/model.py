from database.database import Base
from sqlalchemy import *
from datetime import datetime,timezone
from sqlalchemy.orm import Relationship

class Like_model(Base):
    __tablename__ = "like"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    user = Relationship("User_model")
    post_id = Column(Integer,ForeignKey('posts.id'))
    post = Relationship("Post_model")
    created_at = Column(DateTime,default=datetime.now(tz=timezone.utc))