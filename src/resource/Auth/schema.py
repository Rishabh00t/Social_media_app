from pydantic import BaseModel,EmailStr
from datetime import datetime

class userCreate_schema(BaseModel):
    username:str
    password:str
    email:EmailStr

class UserResponse_schema(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at:datetime
    is_verified:bool
    is_deleted: bool

class Login_schema(BaseModel):
    username:str
    password:str

class UserOTP_schema(BaseModel):
    user_id:int
    otp:int

class LoginRequest_schema(BaseModel):
    username: str
    password: str

class OTPRequest_schema(BaseModel):
    user_id:int
    otp:int

class Token_schema(BaseModel):
    access_token: str
    token_type: str

class DeleteUserRequest_schema(BaseModel):
    token:str
    user_id:int

class PasswordForgot_schema(BaseModel):
    email:EmailStr
class Resetpassword_schema(BaseModel):
    email:EmailStr
    new_password:str