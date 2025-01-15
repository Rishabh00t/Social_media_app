from pydantic import BaseModel

class Create_comment_schema(BaseModel):
    user_id:int
    post_id:int
    text :str

class Delete_comment_schema(BaseModel):
    comment_id:int

class Get_comment_schema(BaseModel):
    comment_id:int