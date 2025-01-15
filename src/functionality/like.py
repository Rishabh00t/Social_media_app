from sqlalchemy.orm import Session
from src.resource.like.model import Like
from src.resource.Post.model import Post
from fastapi import HTTPException,status
import uuid


def post_like(db: Session, postid: str, userid: str):
    try:
        data = db.query(Post).filter(Post.id == postid).one()
        data.likes += 1
        db.commit()

        like_data = Like(id=str(uuid.uuid4()), post_id=postid, user_id=userid)
        db.add(like_data)
        db.commit()
        db.refresh(like_data)
        return True
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))