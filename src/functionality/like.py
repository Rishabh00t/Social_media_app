from sqlalchemy.orm import Session
from src.resource.Auth.model import User_model
from src.resource.Post.model import Post_model
from src.resource.like.model import Like_model
from fastapi import HTTPException,Depends
from datetime import datetime
from database.database import get_db
from src.resource.like.schema import LikeCreate_schema


def create_post_like(post_like:LikeCreate_schema,db:Session=Depends(get_db)):
    try:
        user = db.query(User_model).filter(User_model.id == post_like.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        post = db.query(Post_model).filter(Post_model.id == post_like.post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        db_like=Like_model(
            user_id = post_like.user_id,
            post_id = post_like.post_id,
            created_at=datetime.utcnow()
        )
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return {
            "success":True,
            "message":"Post like successfully!!",
            "like_id":db_like.id,
            "user_id":db_like.user_id,
            "post_id":db_like.post_id
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))