from fastapi_mail import FastMail, MessageSchema
import random
from src.resource.Auth.model import User_model, OTP_model
from sqlalchemy.exc import SQLAlchemyError
import jwt
from datetime import datetime,timedelta
from fastapi import HTTPException, status
from pydantic import EmailStr
from src.utils.user import conf,password_hash
from src.resource.Auth.schema import Resetpassword_schema,DeleteUserRequest_schema
from src.config import SECRET_KEY ,ALGORITHM ,ACCESS_TOKEN_EXPIRE_MINUTES
from src.utils.user import create_access_token,verify_token


async def send_otp_email(otp_code: str, email: str):
    try:
        message = MessageSchema(
            subject="Your OTP Code",
            recipients=[email],
            body=f"Your OTP code is: {otp_code}. It will expire in 5 minutes.",
            subtype="plain"
        )
       
        fm = FastMail(conf)
        await fm.send_message(message)
        return {"success":True}
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return {"success": False, "message": "Failed to send OTP email."}

async def signup(user, db):
    #breakpoint()
    try:
        hashed_password = password_hash.hash(user.password)
        exist_user = db.query(User_model).filter(User_model.username == user.username).first()
        if exist_user:
            raise HTTPException(status_code=400,detail=f"User Already Exist!")
        
        
        exist_mail = db.query(User_model).filter(User_model.email == user.email).first()
        if exist_mail:
             raise HTTPException(status_code=400,detail=f"User Already Exist!")

        db_user = User_model(username=user.username, password=hashed_password, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        otp_code = str(random.randint(100000, 999999))
        expire = datetime.utcnow() + timedelta(minutes=5)
        otp_entry = OTP_model(user_id=db_user.id, otp_code=otp_code, expire_at=expire)
        db.add(otp_entry) 
        db.commit()

        
        send_email_response = await send_otp_email(otp_code, user.email)
        if send_email_response and not send_email_response.get("success", True):
            return send_email_response
        
        token = create_access_token(data={"sub": db_user.username, "id": db_user.id})

        return {
            "success": True,
            "message": "Account successfully created. OTP has been sent, and expires in 5 minutes.",
            "user": {
                "id": db_user.id,
                "username": db_user.username,
                "otp_code": otp_code,
                "email":db_user.email
            },
            "Access-token":token
        }
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error during signup: {e}")
        return {"success": False, "message": "Database error occurred during signup."}
    except Exception as e:
        print(f"Unexpected error during signup: {e}")
    return {"success": False, "message": f"An unexpected error occurred during signup."}

def login(username: str, password: str, db):
    try:
        user_data = db.query(User_model).filter(User_model.username == username).first()

        if user_data:
            if not user_data.is_verified:
                return {
                    "success": False,
                    "message": "User is not verified. Please complete OTP verification first."
                }

            if password_hash.verify(password, user_data.password):

                token = create_access_token(data={"sub": user_data.username, "id": user_data.id})
                return {
                    "success": True,
                    "message": "You are successfully logged in.",
                    "user": {
                        "username": user_data.username,
                        "password": user_data.password,
                        "email": user_data.email,
                        "created_at": user_data.created_at,
                        "is_deleted": user_data.is_deleted,
                    },
                    "token":token
                }

        return {"success": False, "message": "Invalid username or password."}
    except SQLAlchemyError as e:
        print(f"Database error during login: {e}")
        return {"success": False, "message": "Database error occurred during login."}
    except Exception as e:
        print(f"Unexpected error during login: {e}")
        return {"success": False, "message": "An unexpected error occurred during login."}

def verify_otp(user_id:int , otp_code: int, db):
    try:
        otp_entry = db.query(OTP_model).filter(OTP_model.user_id == user_id).first()

        user_data = db.query(User_model).filter(User_model.id == user_id).first()
        if not user_data:
                 return {"success": False, "message": "User not found for the given email."}

        if user_data:
                user_data.is_verified = True
                db.delete(otp_entry)
                db.commit()
                return {"success": True, "message": "OTP verified successfully"}
        
        return {"success": False, "message": "Wrong OTP, please enter the correct OTP."}
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error during OTP verification: {e}")
        return {"success": False, "message": "Database error occurred during OTP verification."}
    except Exception as e:
        print(f"Unexpected error during OTP verification: {e}")
        return {"success": False, "message": "An unexpected error occurred during OTP verification."}
    

def delete_user(request: DeleteUserRequest_schema, db):
    
    try:
        current_user = verify_token(request.token)
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired token. Please log in again."
        )

    if current_user["id"] != request.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user."
        )

    user = db.query(User_model).filter(User_model.id == request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {request.user_id} not found"
        )
    db.delete(user)
    db.commit()
    return {"success": True, "message": f"User with ID {request.user_id} successfully deleted."}



async def passwordforgot(email: EmailStr, db):
    try:
        user1 = db.query(User_model).filter(User_model.email == email).first()
        if not user1:
            raise HTTPException(status_code=404, detail="User with this email does not exist.")
    
        otp_code = str(random.randint(100000, 999999))
        expire = datetime.utcnow() + timedelta(minutes=5)
    
        otp_entry = OTP_model(user_id=user1.id, otp_code=otp_code, expire_at=expire)
        db.add(otp_entry)
        db.commit()

        send_email_response = await send_otp_email(otp_code, user1.email)
        if send_email_response and not send_email_response.get("success", True):
            return send_email_response
        
        return {
            "success": True,
            "message": "OTP has been sent, and expires in 5 minutes. Go and create a new password.",
            "user": {
                "Email": user1.email,
                "otp_code": otp_code,
                "user_id":user1.id
            },
        }
    
    except SQLAlchemyError as e:
        print(f"Database error during sending the OTP: {e}")
        return {"success": False, "message": "Database error occurred during sending the OTP for new password."}
    
    except Exception as e:
        print(f"Unexpected error during sending the OTP: {e}")
        return {"success": False, "message": "An unexpected error occurred during sending the OTP for new password."}

    
def resetpassword(request:Resetpassword_schema,db):
    try:
        user = db.query(User_model).filter(User_model.email == request.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User with this email does not exist.")

        hashed_password = password_hash.hash(request.new_password)
        user.password = hashed_password
        db.commit()

        if user:
            if not user.is_verified:
                return {
                    "success": False,
                    "message": "User is not verified. Please complete OTP verification first."
                }

        return {"success": True, "message": "Password has been reset successfully."}
    except SQLAlchemyError as e:
        print(f"Database error during change password: {e}")
        return {"success": False, "message": "Database error occurred during change password."}
    except Exception as e:
        print(f"Database error during change the password {e}")
        return {"success": False, "message": "An unexpected error occurred during change password."}        