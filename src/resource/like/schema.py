from pydantic import BaseModel
from typing import List, Optional


# Like schema for input when creating a like
class LikeCreate(BaseModel):
    user_id: int
    post_id: int


# Like schema for output after creating a like
class Like(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: str  

# Post like count schema for output
class PostLikeCount(BaseModel):
    post_id: int
    likes_count: int
