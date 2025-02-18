from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from src.resource.like.schema import LikeCreate_schema,Dislike_schema
from sqlalchemy.orm import Session
from database.database import get_db
from src.functionality.like import create_post_like,dislike

like_router = APIRouter(tags=["PostLike Management"])

@like_router.post("/create_like_post")
def user_post_like_create(post_like:LikeCreate_schema,db:Session=Depends(get_db)):
    try:
        demo_like = create_post_like(post_like=post_like,db=db)
        return demo_like
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
@like_router.delete("/dislike_post")
def user_post_dislike(post_dislike:Dislike_schema,db:Session=Depends(get_db)):
    try:
        demo_dislike = dislike(post_dislike=post_dislike,db=db)
        return demo_dislike
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))