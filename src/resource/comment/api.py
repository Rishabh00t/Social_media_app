from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from database.database import get_db
from src.resource.comment.schema import Create_comment_schema,Delete_comment_schema,Get_comment_schema
from src.functionality.comment import create_comment,delete_comment,get_comment_by_id

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