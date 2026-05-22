from pydantic import BaseModel, EmailStr 
from typing import Optional
from datetime import datetime


class CreatePost(BaseModel):
    id: int
    title: str
    content: str


class UpdatePost(BaseModel):
    title: str
    content: str

class PostResponse(UpdatePost):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    class Config:
        from_attributes = True


class UserPostResponse(UpdatePost):
    id : int
    created_at: datetime

    class Config:
        from_attributes = True
        
class CreateUser(BaseModel):
    user_id : int
    email : EmailStr
    password : str

class UserOut(BaseModel):
    user_id:int
    email:EmailStr
    
    class config:
        from_attributes = True
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    id : Optional[int] = None
