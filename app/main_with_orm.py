from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.params import Body
from typing import List
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import engine, Base, get_db
from .models import Post
import time
from sqlalchemy.orm import Session
from .schemas import CreatePost,UpdatePost , PostResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

# testing


@app.get("/testing")
def get(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


# title->str and content->str

@app.get("/", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
async def root(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts



@app.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    if post is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    new_post = Post(
        id=post.id,
        title=post.title,
        content=post.content
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": f"successfully cre ated the post named \"{post.title}\""}


@app.get("/post/{id}",  status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id)
    post.delete(synchronize_session=False)
    db.commit()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return


@app.put("/update/{id}", status_code=status.HTTP_205_RESET_CONTENT)
def update(id: int, post: UpdatePost, db: Session = Depends(get_db)):

    post_query = db.query(Post).filter(Post.id == id)

    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    post_query.update(
        {
            "title": post.title,
            "content": post.content,
            "rating": post.rating
        }
    )

    db.commit()

    return {"message": "Successfully updated"}
