from .database import Base
from sqlalchemy import Column, Integer, String, Boolean


class NewPost(Base):
    __tablename__ = "newposts" 
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String(100), nullable=False)
    published = Column(Boolean, default=True) 
