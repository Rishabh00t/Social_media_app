from pydantic import BaseModel



class LikeCreate_schema(BaseModel):
    user_id: int
    post_id: int



class Like_Response(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: str  

class Dislike_schema(BaseModel):
    like_id:int
    post_id:int