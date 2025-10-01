from pydantic import BaseModel, ConfigDict, EmailStr, conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
  title : str
  content : str
  published : bool = False


class PostCreate(PostBase):
  pass

class User(BaseModel):
  id : int
  email : EmailStr
  created_at : datetime

  model_config = ConfigDict(from_attributes=True)

class UserFetch(BaseModel):
  email : EmailStr


class Post(PostBase):
  id : int
  owner_id : int
  created_at : datetime
  owner : UserFetch
  
  model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
  email : EmailStr
  password : str



class UserAuth(BaseModel):
  email : EmailStr
  password : str


class Token(BaseModel):
  access_token : str
  token_type : str

class TokenData(BaseModel):
  id : Optional[int] = None


class Vote(BaseModel):
  post_id: int
  dir: conint(ge=0, le=1) # type: ignore


class PostOut(BaseModel):
  Post : Post
  likes : int
  model_config = ConfigDict(from_attributes=True)
