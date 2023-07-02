from fastapi import FastAPI, Form, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db
from app import utils


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("/", response_model=schemas.PostOut, status_code=201)
def create_post(post: schemas.Post,
                    user:schemas.TokenData=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    
    if db.query(models.Post).filter(models.Post.post == post.post, models.Post.election_id == post.election_id).first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Post with name {post.post} already exists")
    user_elections = db.query(models.Election).filter(
        models.Election.id == post.election_id, models.Election.creator_id == int(user.id)).first()
    if not user_elections:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, user:schemas.TokenData=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with {id} not found")
    user_elections = db.query(models.Election).join(models.Post).filter(
        models.Post.id == id, models.Election.creator_id == int(user.id)).first()
    if not user_elections:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    post_query.delete(synchronize_session=False)
    db.commit()
    return 
