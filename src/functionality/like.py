from sqlalchemy.orm import Session
from src.resource.Auth.model import User_model
from src.resource.Post.model import Post_model
from src.resource.like.model import Like_model
from fastapi import HTTPException,Depends,status
from datetime import datetime
from database.database import get_db
from src.resource.like.schema import LikeCreate_schema,Dislike_schema


def create_post_like(post_like: LikeCreate_schema, db: Session = Depends(get_db)):
    try:
        
        user = db.query(User_model).filter(User_model.id == post_like.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        post = db.query(Post_model).filter(Post_model.id == post_like.post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        existing_like = db.query(Like_model).filter(
            Like_model.user_id == post_like.user_id,
            Like_model.post_id == post_like.post_id
        ).first()
        if existing_like:
            raise HTTPException(status_code=400, detail="Already liked this post")

        db_like = Like_model(
            user_id=post_like.user_id,
            post_id=post_like.post_id,
            created_at=datetime.utcnow()    
        )
        db.add(db_like)

        post.like_count = (post.like_count or 0) + 1
        db.commit()
        db.refresh(db_like)

        return {
            "success": True,
            "message": "Post liked successfully!!",
            "like_id": db_like.id,
            "user_id": db_like.user_id,
            "post_id": db_like.post_id,
            "like_count": post.like_count  
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def dislike(post_dislike : Dislike_schema,db:Session=Depends(get_db)):
    try:
        # breakpoint()
        post = db.query(Post_model).filter(Post_model.id == post_dislike.post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        like = db.query(Like_model).filter(Like_model.id == post_dislike.like_id).first()
        if not like:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Like with ID {post_dislike.like_id} not found"
                )
        db.delete(like)
        db.commit()
        # db.refresh(like)

        post.like_count = (post.like_count or 0) - 1
        db.commit()
        db.refresh(like)
        return {"success": True, "message": f"User with like ID {post_dislike.like_id} successfully dislike the post."}
    except Exception as e:
        raise HTTPException(
            status_code=500,detail=str(e)
        )