from pydantic import BaseModel,EmailStr

class View_profile_schema(BaseModel):
    username:str

class Update_profile_schema(BaseModel):
    user_id:int
    username:str
    password:str
    email:EmailStr