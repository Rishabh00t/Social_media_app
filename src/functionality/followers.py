from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from src.resource.Auth.model import User_model
from src.resource.followers.schemas import Follower_schema,Unfollow_schema,Get_follower_schema
from database.database import get_db
from src.resource.followers.model import Follower_model
from datetime import datetime

def create_follower(follower:Follower_schema,db:Session=Depends(get_db)):
    try: 
        user = db.query(User_model).filter(User_model.id == follower.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        follow_data = db.query(User_model).filter(User_model.id == follower.follower_id).first()
        if not follow_data:
            raise HTTPException(status_code=404,detail="follower not found!")
        
        db_follower=Follower_model(
            user_id=follower.user_id,
            follower_id=follower.follower_id,
            created_at=datetime.utcnow()
        )
        db.add(db_follower)

        user.followers_count = (user.followers_count or 0) +1
        db.commit()
        db.refresh(db_follower)

        return {
            "success":True,
            "message":f"you successfully followed user whoses user_id is {follower.follower_id}."
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
def unfollow(unfollow_user:Unfollow_schema,db:Session=Depends(get_db)):
    try:
        user = db.query(User_model).filter(User_model.id == unfollow_user.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        unfollow_data = db.query(Follower_model).filter(Follower_model.follower_id == unfollow_user.follower_id).first()
        if not unfollow_data:
            raise HTTPException(status_code=404,detail="follower not found!")
        
        db.delete(unfollow_data)
        db.commit()

        user.followers_count = (user.followers_count or 0) -1
        db.commit()
        # db.refresh(unfollow_data)
        return {
            "success":True,
            "message":f"you successfully unfollowed user whoses user_id is {unfollow_user.user_id}."
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    

def get_all_follower(fetch_follower:Get_follower_schema,db:Session=Depends(get_db)):
    try:
        user = db.query(User_model).filter(User_model.id == fetch_follower.user_id).first()
        return {
            "success":True,
            "message":"All Followers of this user..",
            "Follower_count":user.followers_count
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))