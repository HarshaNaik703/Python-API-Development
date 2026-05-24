from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from ..models import Post,Vote,User
from ..schemas import PostResponse

router = APIRouter(prefix="/votes", tags=["Likes"])

@router.post("/{id}", status_code=status.HTTP_200_OK)
async def put_like(id:int, user : int = Depends(get_current_user), db : Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    like = db.query(Vote).filter(Vote.post_id == id).filter(
        Vote.user_id == user.user_id)
    if like.first() is not None:
        like.delete(synchronize_session=False)
        db.commit()
        return {"message":"you disliked this post"}
    else:
        like = Vote(
            user_id = user.user_id,
            post_id = post.id
        )
        db.add(like)
        db.commit()
        db.refresh(like)
        return {"message":"You successfully like this post"}
    
