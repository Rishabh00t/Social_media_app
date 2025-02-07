from database.database import Base
from sqlalchemy import *
from datetime import datetime,timezone
from sqlalchemy.orm import Relationship

class Like_model(Base):
    __tablename__ = "like"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id',ondelete='cascade'))
    user = Relationship("User_model")
    post_id = Column(Integer,ForeignKey('posts.id',ondelete='cascade'))
    post = Relationship("Post_model")
    created_at = Column(DateTime,default=datetime.now(tz=timezone.utc))
    # updated_at = Column(DateTime,default=datetime.now(tz=timezone.utc))