from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from src.resource.followers.schemas import Follower_schema,Unfollow_schema,Get_follower_schema
from database.database import get_db
from src.functionality.followers import create_follower,unfollow,get_all_follower

follower_router = APIRouter()

@follower_router.post("/follow_user")
def follow_user(follower:Follower_schema,db:Session=Depends(get_db)):
    try:
        response = create_follower(follower=follower,db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    

@follower_router.delete("/unfollow")
def unfollow_user_id(unfollow_user:Unfollow_schema,db:Session=Depends(get_db)):
    try:
        response = unfollow(unfollow_user=unfollow_user,db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@follower_router.get("/follower_count")
def fetch_all_follower(fetch_follower:Get_follower_schema,db:Session=Depends(get_db)):
    try:
        response = get_all_follower(fetch_follower=fetch_follower,db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))