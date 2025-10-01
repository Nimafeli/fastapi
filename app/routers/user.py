from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model = schemas.User)
async def cerate_user(user: schemas.UserCreate, db : Session = Depends(get_db)):

    #hash the password - user.password
    user.password = utils.hash(user.password)
    new_uesr = models.User(**user.__dict__)
    db.add(new_uesr)
    db.commit()
    db.refresh(new_uesr)

    return new_uesr


@router.get('/{id}', response_model = schemas.User)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"There is no user wiht id = {id}")
    
    return user