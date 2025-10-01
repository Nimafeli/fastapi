from datetime import datetime, timedelta
from jose import jwt, JWTError
from . import schemas, models, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#ALgorithm
#expiration time

SECRECT_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict):
  to_encode = data.copy()

  expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})

  encoded_jwt = jwt.encode(to_encode, SECRECT_KEY, algorithm=ALGORITHM)

  return encoded_jwt


def verify_acces_token(token : str, credentials_execption):

  try:
    payload = jwt.decode(token, SECRECT_KEY, algorithms=[ALGORITHM])

    id = payload.get("user_id")

    if id is None:
      raise credentials_execption
    token_data = schemas.TokenData(id = id)
  except JWTError :
    raise credentials_execption
  
  return token_data
  

def get_current_user(token : str = Depends(oauth2_schema), db : Session = Depends(database.get_db)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
  returned_token = verify_acces_token(token, credentials_exception)
  user = db.query(models.User).filter(models.User.id == returned_token.id).first()

  return user