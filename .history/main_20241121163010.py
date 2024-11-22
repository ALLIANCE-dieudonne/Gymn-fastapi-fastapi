from fastapi import FastAPI, HTTPException,Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserBase(BaseModel):
    username: str
    email: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully"}

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Posts(title=post.title, content=post.content, published=post.published)
    db.add(db_post)
    db.commit()
    return {"message": "Post created successfully"}

@app.get("/posts/{post_id}")
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/posts/")
async def read_all_posts(db: db_dependency):
    posts = db.query(models.Posts).all()
    return posts

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: db_dependency):
    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return None

@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: PostBase, db: db_dependency):
    db_post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published
    
    db.commit()
    return {"message": "Post updated successfully"}

