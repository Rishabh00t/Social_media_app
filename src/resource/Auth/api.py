from fastapi import Depends,APIRouter,HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from src.resource.Auth.model import User_model
from src.functionality.auth import signup
from src.resource.Auth.schema import userCreate_schema
from src.functionality.auth import login,verify_otp,verify_token,delete_user,passwordforgot,resetpassword
from src.resource.Auth.schema import LoginRequest_schema,OTPRequest_schema,PasswordForgot_schema,Resetpassword_schema
from fastapi import Depends
from src.resource.Auth.token import oauth2_scheme
from fastapi import Security
from fastapi.security import HTTPBearer

security = HTTPBearer()

auth_router=APIRouter(tags=["Users_Authentication"])

@auth_router.post("/signup")
async def create_user(user: userCreate_schema, db: Session = Depends(get_db)):
    try:
        response = await signup(user,db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@auth_router.get("/users")
async def get_users(db: Session = Depends(get_db)):   
    users = db.query(User_model).all()
    return {"success": True, "users": users}

@auth_router.post("/login")
async def get_user(request: LoginRequest_schema,db:Session=Depends(get_db)):
    response = login(request.username,request.password,db)
    return response

@auth_router.post("/verifyOTP")
async def verify_userotp(request:OTPRequest_schema ,db:Session=Depends(get_db)):
    response1 = verify_otp(request.user_id,request.otp,db)
    return response1

@auth_router.get("/protected-route")
async def protected_route(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    return {"success": True, "message": "Access granted", "user": user}

@auth_router.delete("/deleteuser/{user_id}")
async def deleteUser(user_id:int,db:Session=Depends(get_db),token: str = Security(security)):
    response=delete_user(user_id=user_id,db=db,token=token)
    return response

@auth_router.post("/forgotpassword")
async def forgotPassword(request:PasswordForgot_schema,db:Session=Depends(get_db)):
    response = await passwordforgot(request.email,db)
    return response

@auth_router.post("/resetPassword")
def reset_password(request:Resetpassword_schema,db:Session=Depends(get_db)):
    response = resetpassword(request,db)
    return response