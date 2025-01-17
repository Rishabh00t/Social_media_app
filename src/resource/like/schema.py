from pydantic import BaseModel
from typing import List, Optional



class LikeCreate_schema(BaseModel):
    user_id: int
    post_id: int



class Like(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: str  

class Dislike_schema(BaseModel):
    like_id:int
    post_id:int