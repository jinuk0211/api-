from typing import List, Optional, conint
from pydantic import BaseModel, EmailStr
from datetime import datetime
import conint

class PostBase(BaseModel): #데이터베이스에 저장할 데이터 형식
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass    

class Post(PostBase):#데이터베이스에서 가져올 데이터 형식
    title: str
    content: str
    published: bool 
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class TokenData(BaseModel):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str
    
class Vote(BaseModel):
    post_id: int
    dir : conint(le=1)#1이하의 정수
    