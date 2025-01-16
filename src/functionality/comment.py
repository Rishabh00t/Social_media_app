from database.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from datetime import datetime
from src.resource.comment.model import Comment_model
from src.resource.Auth.model import User_model
from src.resource.Post.model import Post_model
from src.resource.comment.model import Comment_like
from src.resource.comment.schema import Comment_like_schema

def create_comment(comment, db: Session = Depends(get_db)):
    try:
        
        exist_user = db.query(User_model).filter(User_model.id == comment.user_id).first()
        if not exist_user:
            return {"error": "User ID not found"}

        exist_post = db.query(Post_model).filter(Post_model.id == comment.post_id).first()
        if not exist_post:
            return {"error": "Post ID not found"}

        comment_data = Comment_model(
            user_id=comment.user_id, post_id=comment.post_id, text=comment.text
        )
        db.add(comment_data)
        db.commit()
        return {"success":True,
            "message": "Comment created successfully",
            "User_id":comment_data.user_id,
            "post_id":comment_data.post_id,
            "Comment":comment_data.text

             }
    except Exception as e:
        print(f"Comment not created. {e}")
        return {"error": f"An error occurred: {e}"}
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    try:

        comment = db.query(Comment_model).filter(Comment_model.id == comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment with ID {comment_id} not found."
            )
        
        db.delete(comment)
        db.commit()
        return {"success": True, "message": f"Comment with ID {comment_id} successfully deleted."}
    except Exception as e:
        print(f"Unexpected error during deleting the user's comment: {e}")
        return {"success": False, "message": "An unexpected error occurred during deleting the user's comment."}
    
def get_comment_by_id(comment_id,db:Session=Depends(get_db)):
    try:
        comment_data = db.query(Comment_model).filter(Comment_model.id == comment_id).first()
        # breakpoint()
        if not comment_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {comment_id} not found"
            )
        
        return {
            "Success":True,
            "message":"comment found successfully..",
            "Comment_id" : comment_data.id,
            "post_id" : comment_data.post_id,
            "captions":comment_data.text,
            "created_at":comment_data.created_at
        }
    except Exception as e:
        print(f"Unexpected error during fetching the user's comment: {e}")
        return {"success": False, "message": "An unexpected error occurred during fetching the user's comment."}
    
""" def comment_like(comment_id:int,post_id:int,user_id:int,db:Session=Depends(get_db)):
    try:
        # #breakpoint()
        # data = db.query(Comment_model).filter(Comment_model.id == comment_id)
        # data.likes +=1
        # db.commit()

        like_comment = comment_like(comment_id=comment_id,user_id=user_id,post_id=post_id)
        db.add(like_comment)
        db.commit()
        db.refresh(like_comment)
        return {"success":True}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) """

def create_like(like: Comment_like_schema, db: Session = Depends(get_db)):
    try:
        user = db.query(User_model).filter(User_model.id == like.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if like.post_id:
            post = db.query(Post_model).filter(Post_model.id == like.post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        if like.comment_id:
            comment = db.query(Comment_model).filter(Comment_model.id == like.comment_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
    
        db_like = Comment_like(
            post_id=like.post_id,
            comment_id=like.comment_id,
            user_id=like.user_id,
            created_at=datetime.utcnow()
            )
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return {"Status":"Success",
            "message": "Like created successfully",
            "data":{
            "like_id": db_like.id,
            "user_id":db_like.user_id,
            "comment_id" : db_like.comment_id,
            "post_id": db_like.post_id
             }
            }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))