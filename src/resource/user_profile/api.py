from fastapi import APIRouter,HTTPException,Depends,Security
from database.database import get_db
from src.resource.user_profile.schema import View_profile_schema,Update_profile_schema
from sqlalchemy.orm import Session
from src.functionality.profile_view import view_profile_user,update_profile

from fastapi.security import HTTPBearer

security = HTTPBearer()


user_router = APIRouter()

@user_router.get("/view_profile")
def view_user_profile(profile:View_profile_schema,db:Session=Depends(get_db)):
    try:
        response = view_profile_user(profile.username,db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@user_router.patch("/edit_profile")
def eddit_profile(update_profile_user:Update_profile_schema,db:Session=Depends(get_db),token: str = Security(security)):
    try:
        response = update_profile(update_profile_user,db,token)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))