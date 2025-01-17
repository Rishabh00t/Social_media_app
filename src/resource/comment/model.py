from sqlalchemy import *
from database.database import Base
from datetime import datetime , timezone
from sqlalchemy.orm import Relationship

class Comment_model(Base):
    __tablename__ = "comments"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete='cascade'))
    user = Relationship("User_model")
    post_id = Column(Integer,ForeignKey("posts.id",ondelete='cascade'))
    post = Relationship("Post_model")
    text = Column(String(255))
    likes = Column(Integer,default=0)
    created_at = Column(DateTime,default=datetime.now(tz=timezone.utc))
    is_deleted = Column(Boolean,default=False)

class Comment_like(Base):
    __tablename__ = "comment_like"
    id = Column(Integer,primary_key=True)
    comment_id = Column(Integer,ForeignKey("comments.id",ondelete='cascade'))
    comment = Relationship("Comment_model")
    post_id = Column(Integer,ForeignKey("posts.id",ondelete='cascade'))
    post = Relationship("Post_model")
    user_id = Column(Integer,ForeignKey("users.id",ondelete='cascade'))
    user = Relationship("User_model")
    created_at = Column(DateTime,default=datetime.now(tz=timezone.utc))