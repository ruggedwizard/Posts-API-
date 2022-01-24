from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at = datetime

    class Config:
        orm_mode = True

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    owner_id:int
    owner:UserOut


    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    password:str


class User(UserBase):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None

