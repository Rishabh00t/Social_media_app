from fastapi import HTTPException,Depends,status,Security
from src.resource.user_profile.schema import View_profile_schema,Update_profile_schema
from sqlalchemy.orm import Session
from database.database import get_db
from src.resource.Auth.model import User_model
from src.utils.user import password_hash,verify_token
from fastapi.security import HTTPBearer

security = HTTPBearer()

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
    
def update_profile(update_profile:Update_profile_schema,db:Depends=Session(get_db),token: str = Security(security)):
    try:
        try:
            current_user = verify_token(token.credentials)
        except HTTPException as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token. Please log in again."
        )
        if current_user["id"] != update_profile.user_id:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user."
        )
        user=db.query(User_model).filter(User_model.id == update_profile.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {update_profile.user_id} not found"
            )
        if update_profile.username is not None:
            user.username = update_profile.username
        if update_profile.password is not None:
            user.password = password_hash.hash(update_profile.password)
        if update_profile.email is not None:
            user.email = update_profile.email
        db.commit()
        return {
            "success":True,
            "message":"profile edited successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))