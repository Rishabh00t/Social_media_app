from fastapi import HTTPException,Depends
from src.resource.user_profile.schema import View_profile
from sqlalchemy.orm import Session
from database.database import get_db
from src.resource.Auth.model import User_model

def view_profile_user(username: str, db: Session = Depends(get_db)):
    try: 
        user_data = db.query(User_model).filter(User_model.username == username).first()

        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "success": True,
            "user": {
                "username": user_data.username,
                "email": user_data.email,
                "created_at": user_data.created_at,
                "is_deleted": user_data.is_deleted,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))