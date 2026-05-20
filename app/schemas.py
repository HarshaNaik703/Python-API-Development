from pydantic import BaseModel
from datetime import datetime


class CreatePost(BaseModel):
    id: int
    title: str
    content: str


class UpdatePost(BaseModel):
    title: str
    content: str

class PostResponse(UpdatePost):
    create_at : datetime
    class Config:
        from_attributes = True
