from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy import exc
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db
from app import utils


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=201, response_model=schemas.Token)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except exc.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="user with email already exists")
    access_token = oauth2.create_access_token(data={"user_id": new_user.id})

    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user

@router.get('/')
def get_login_user(user = Depends(oauth2.get_current_user)):
    return user