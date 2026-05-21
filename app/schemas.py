from pydantic import BaseModel, EmailStr
from datetime import datetime


class CreatePost(BaseModel):
    id: int
    title: str
    content: str


class UpdatePost(BaseModel):
    title: str
    content: str

class PostResponse(UpdatePost):
    created_at : datetime
    class Config:
        from_attributes = True
        
class CreateUser(BaseModel):
    id : int
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    
    class config:
        from_attributes = True
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str
