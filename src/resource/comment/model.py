from sqlalchemy import *
from database.database import Base
from datetime import datetime , timezone
from sqlalchemy.orm import Relationship

class Comment_model(Base):
    __tablename__ = "comments"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    user = Relationship("User_model")
    post_id = Column(Integer,ForeignKey("posts.id"))
    post = Relationship("Post_model")
    text = Column(String(255))
    created_at = Column(DateTime,default=datetime.now(tz=timezone.utc))
    is_deleted = Column(Boolean,default=False)