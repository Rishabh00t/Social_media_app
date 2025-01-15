from fastapi import Depends,APIRouter,UploadFile,File,Form,HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from src.functionality.post import create_post,get_post_by_id,delete_post,update_post
from src.resource.Post.schema import GetPost_schema,DeletePost_schema,Updatepost_schema,Postcreate_schema
from src.resource.Post.model import Post_model

post_router=APIRouter()

@post_router.post("/create_post/")
def create_user_post(
    token :str = Form(...),
    user_id: int = Form(...),
    title: str = Form(...),
    captions: str = Form(...),
    db: Session = Depends(get_db),
    image: UploadFile = File(...)):
    try:
        post_data = Postcreate_schema(title=title, captions=captions, user_id=user_id , token=token)
        post = create_post(post=post_data,db=db,image=image)
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@post_router.get("/get_posts")
async def get_users(db: Session = Depends(get_db)):   
    posts = db.query(Post_model).all()
    return {"success": True, "users": posts}

@post_router.get("/get_post_by_ID")
def get_user_post(request:GetPost_schema,db:Session=Depends(get_db)):
    response = get_post_by_id(request,db)
    return response

@post_router.delete("/delete_post")
def delete_user_post(request:DeletePost_schema,db:Session=Depends(get_db)):
    response = delete_post(request.post_id,db)
    return response
@post_router.patch("/update_post")
def update_user_post(request:Updatepost_schema,db:Session=Depends(get_db)):
    response = update_post(request.post_id,request,db)
    return response