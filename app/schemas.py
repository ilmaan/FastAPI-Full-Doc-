from pydantic import BaseModel
from typing import Optional
from datetime import datetime




class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
    


class CreatePost(BaseModel):
    pass


class UpdatePost(BaseModel):
    content : str
    published : bool = True



class PostOut(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True
