from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List


from ..database import get_db
from ..models import Post
from ..schemas import PostResponse, CreatePost, UpdatePost

router = APIRouter(prefix="/posts", tags=["Post"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
async def root(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@router.post("/create_post", status_code=status.HTTP_201_CREATED)
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


@router.get("/{id}",  status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id)
    post.delete(synchronize_session=False)
    db.commit()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return


@router.put("/update/{id}", status_code=status.HTTP_205_RESET_CONTENT)
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
