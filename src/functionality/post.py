from fastapi import Depends,HTTPException,status,File,UploadFile
from src.resource.Post.model import Post_model
from random import randint
from database.database import get_db
from sqlalchemy.orm import Session
from src.resource.Post.schema import Updatepost_schema,Postcreate_schema
IMAGEDIR = "image/"
import uuid ,os
from src.functionality.auth import verify_token

def create_post(post:Postcreate_schema, db: Session = Depends(get_db), image: UploadFile = File(...)):
    try:
        current_user = verify_token(post.token)
       

        if current_user["id"] != post.user_id:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user."
            )

        # breakpoint()
        file_extension = image.filename.split('.')[-1]
        image.filename = f"{uuid.uuid4()}.{file_extension}"
        

        file_path = f"{IMAGEDIR}/{image.filename}"
        contents = image.file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        db_post = Post_model(
            user_id=current_user["id"],
            title=post.title,
            captions=post.captions,
            image_url=file_path
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        
        return {"success": True,
                "message": "Post created successfully",
                "filepath": file_path}
    except Exception:
        return {"success": False, "message": "An unexpected error occurred during post creation"}


def get_post_by_id(get_user, db: Session = Depends(get_db)):
    try:

        files = os.listdir(IMAGEDIR)

        random_index = randint(0, len(files) - 1)
        path = os.path.join(IMAGEDIR, files[random_index])

        post_id = get_user.post_id
        post_data = db.query(Post_model).filter(Post_model.id == post_id).first()
        if not post_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found"
            )

        return {
            "success": True,
            "message": "Post found successfully!",
            "post_id": post_data.id,
            "Title": post_data.title,
            "captions": post_data.captions,
            "created_at": post_data.created_at,
            "updated_at": post_data.updated_at,
            "file_path": path 
        }
    except Exception as e:
        print(f"Unexpected error during fetching the user`s post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the user’s post."
        )

def delete_post(post_id,db:Session=Depends(get_db)):
    try:
        # breakpoint()
        
        post=db.query(Post_model).filter(Post_model.id == post_id).first()
        if not post:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found"
                )
        db.delete(post)
        db.commit()
        return {"success": True, "message": f"User with ID {post_id} successfully deleted."}
    except Exception as e:
        print(f"Unexpected error during fetching the user`s post: {e}")
        return {"success": False, "message": "An unexpected error occurred during fetching the user`s post."}

def update_post(post_id,update_post:Updatepost_schema,db:Session=Depends(get_db)):
    try:
        # breakpoint()
        post=db.query(Post_model).filter(Post_model.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found"
            )
        if update_post.title is not None:
            post.title=update_post.title
        if update_post.captions is not None:
            post.captions=update_post.captions
        db.commit()
        return {"succcess":True,"message":"Post updated successfully!!",
                "post": {"id": post.id, "Title": post.title, "Captions": post.captions}
                }
    except Exception as e:
        print(f"Unexpected error during updating the user`s post: {e}")
        return {"success": False, "message": "An unexpected error occurred during updating the user`s post."}
