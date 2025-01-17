from pydantic import BaseModel,EmailStr
from datetime import datetime

class Postcreate_schema(BaseModel):
    user_id:int
    title:str
    captions:str

class postresponce(BaseModel):
    id: int
    user_id:int
    title:str
    captions:str
    created_at: datetime
    updated_at:datetime
    is_verified:bool
    is_deleted: bool

class GetPost_schema(BaseModel):
    post_id:int

class DeletePost_schema(BaseModel):
    post_id:int

class Updatepost_schema(BaseModel):
    post_id:int
    title:str | None = None
    captions:str | None = None