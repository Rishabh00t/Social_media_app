from fastapi import Depends,APIRouter,HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from database.database import get_db
from src.resource.comment.schema import Create_comment_schema,Delete_comment_schema,Get_comment_schema,Comment_like_schema,Comment_dislike_schema
from src.functionality.comment import create_comment,delete_comment,get_comment_by_id,create_like,create_dislike

comment_router = APIRouter()

@comment_router.post("/create_comment")
def create_user_comment(request:Create_comment_schema,db:Session=Depends(get_db)):
    response = create_comment(request,db)
    return response

@comment_router.delete("/delete_comment")
def delete_user_comment(request:Delete_comment_schema,db:Session=Depends(get_db)):
    response = delete_comment(request.comment_id,db)
    return response

@comment_router.get("/get_comment")
def get_comment_by_ID(request:Get_comment_schema,db:Session=Depends(get_db)):
    response = get_comment_by_id(request.comment_id,db)
    return response

@comment_router.post("/like_comment")
def create_like_comment(like:Comment_like_schema,db:Session=Depends(get_db)):
    try:
        demo_like= create_like(like=like,db=db)
        return demo_like
    except Exception as e:
       raise HTTPException(status_code=500,detail=str(e))
    
@comment_router.delete("/dislike_comment")
def create_dislike_comment(dislike:Comment_dislike_schema,db:Session=Depends(get_db)):
    try:
        demo_dislike=create_dislike(dislike=dislike,db=db)
        return demo_dislike
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))