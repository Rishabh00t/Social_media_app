from sqlalchemy import *
from database.database import Base
from datetime import datetime,timezone
from sqlalchemy.orm import Relationship

class Follower_model(Base):
    __tablename__ = "followers"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer ,ForeignKey("users.id",ondelete="cascade"))
    # user = Relationship("User_model")
    follower_id = Column(Integer,ForeignKey("users.id",ondelete='cascade'))
    # follow = Relationship("User_model")
    created_at = Column(DateTime,default=datetime.now(tz=timezone.utc))