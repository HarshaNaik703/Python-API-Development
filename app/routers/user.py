from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User
from ..schemas import CreateUser, UserLogin, UserOut
from ..utils import hashing, rehashing

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="details are not enough")
    new_user = User(
        user_id=user.user_id,
        password=hashing(user.password),
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "user created successfully"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user not found of id {id}")
    return user
