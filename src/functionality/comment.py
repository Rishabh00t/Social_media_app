from database.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from src.resource.comment.model import Comment_model
from src.resource.Auth.model import User_model
from src.resource.Post.model import Post_model
from src.resource.comment.model import Comment_model

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