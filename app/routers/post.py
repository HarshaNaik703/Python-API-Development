from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..oauth2 import get_current_user
from sqlalchemy import func
from ..database import get_db
from ..models import Post, Vote
from ..schemas import PostResponse, CreatePost, UpdatePost, UserPostResponse,IndividualPost


router = APIRouter(prefix="/posts", tags=["Post"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
async def root(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.id).all()
    return posts


@router.get("/your_posts", status_code=status.HTTP_200_OK, response_model=List[UserPostResponse])
async def root(db: Session = Depends(get_db), user: int = Depends(get_current_user), limit : int = 1000, skip : int = 0):
    posts = db.query(Post).filter(Post.owner_id == user.user_id).limit(limit).offset(skip).all()
    return posts

@router.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost, db: Session = Depends(get_db), user : int = Depends(get_current_user)):
    if post is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    new_post = Post(
        id=post.id,
        title=post.title,
        content=post.content,
        owner_id = user.user_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": f"successfully cre ated the post named \"{post.title}\""}


@router.get("/{id}",  status_code=status.HTTP_200_OK, response_model=IndividualPost)
def get_post(id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()
    # print(post.get_post())
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorised to see this post")
        
    result = db.query(
        Post.title,
        Post.id,
        func.count(Vote.user_id).label('likes')
    ).outerjoin(Vote, Post.id == Vote.post_id).group_by(
        Post.title,
        Post.id
    ).having(Post.id == id).first()
    print(post.content)
    post.likes = result[2]
    return post


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if post.owner_id == user.user_id:
        post.delete(synchronize_session=False)
        db.commit()
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorised to delete this post")


@router.put("/update/{id}", status_code=status.HTTP_205_RESET_CONTENT)
def update(id: int, post: UpdatePost, db: Session = Depends(get_db), user: int = Depends(get_current_user)):

    post_query = db.query(Post).filter(Post.id == id)

    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if existing_post.owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorised to update this post")

    post_query.update(
        {
            "title": post.title,
            "content": post.content,
            "rating": post.rating
        }
    )

    db.commit()

    return {"message": "Successfully updated"}
