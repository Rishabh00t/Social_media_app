from fastapi import APIRouter,HTTPException,Depends
from database.database import get_db
from src.resource.user_profile.schema import View_profile
from sqlalchemy.orm import Session
from src.functionality.profile_view import view_profile_user


user_router = APIRouter()

@user_router.get("/view_profile")
def view_user_profile(profile:View_profile,db:Session=Depends(get_db)):
    try:
        response = view_profile_user(profile.username,db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))