from pydantic import BaseModel

class Follower_schema(BaseModel):
    user_id:int
    follower_id:int

class Follower_response_schema(BaseModel):
    id:int
    user_id:int
    follower_id:int
    created_at:str

class Unfollow_schema(BaseModel):
    user_id:int
    follower_id:int

class Get_follower_schema(BaseModel):
    user_id:int