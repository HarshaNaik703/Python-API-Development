from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User
from ..schemas import CreateUser, UserLogin, UserOut, PasswordReset, Password
from ..utils import hashing, rehashing, password_check
from ..oauth2 import get_current_user

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="details are not enough")
    new_user = User(
        user_id=user.user_id,
        password=hashing(user.password),
        email=user.email,
        phone_number = user.phone_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "user created successfully"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.user_id).all()
    return users

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user not found of id {id}")
    return user

@router.post("/password_reset", status_code=status.HTTP_200_OK)
def password_reset(password : PasswordReset,user: int = Depends(get_current_user),db: Session = Depends(get_db)):
    if rehashing(password.oldpass, user.password):
        update_user = db.query(User).filter(User.user_id == user.user_id).first()
        old_password = rehashing(password.newpass, user.password)
        
        user_temp = old_password.first()
        password_check(password.newpass, user_temp.password)
        
        db.query(User).filter(User.user_id == user.user_id).update({
            "password": hashing(password.newpass)
        })
        db.commit()
        return {"message": "password updated , login again"}
    else:
        print(user.password)
        print(type(user.password))
        print(rehashing(password.oldpass, user.password))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Password")
    

@router.post("/reset_password", status_code=status.HTTP_200_OK)
def password_reset(password: Password, db: Session = Depends(get_db)):
    if password.email == None and password.user_id is None:
        raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail="Insufficient details")
    if password.email is not None and password.user_id is None:
        user = db.query(User).filter(User.email == password.email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"user not found with email {password.email}")
        password_check(password.newpass, user.password)
        
        db.query(User).filter(User.email == password.email).update({
            "password": hashing(password.newpass)
        })
        db.commit()
        return {"message": "password updated"}
    elif password.user_id is not None and password.email is None:
        user = db.query(User).filter(User.user_id == password.user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"user not found with id {password.user_id}")
        password_check(password.newpass, user.password)
            
        db.query(User).filter(User.user_id == password.user_id).update({
            "password": hashing(password.newpass)
        })
        db.commit()
        return {"message": "password updated"}
    else:
        user_by_id = db.query(User).filter(User.user_id == password.user_id).first()
        user_by_email = db.query(User).filter(User.email == password.email).first()
        
        if user_by_id is None or user_by_email is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if user_by_id.user_id != user_by_email.user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Details mismatching")
        
        password_check(password.newpass, user_by_id.password)
        
        db.query(User).filter(User.email == password.email).update({
            "password": hashing(password.newpass)
        })
        db.commit()
        return {"message": "password updated"}
        


        
        
