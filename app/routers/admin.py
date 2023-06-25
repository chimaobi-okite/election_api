from fastapi import FastAPI, Form, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db
from app import utils


router = APIRouter(
    prefix="/admins",
    tags=['Admin']
)

@router.post("/",status_code=201)
def create_admin(admin: schemas.Admin,
                    user:schemas.TokenData=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    election = db.query(models.Election).filter(models.Election.creator_id == int(user.id),
                                                 models.Election.id == admin.election_id).first()
    if not election:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only election creators can create admins")
    hashed_password = utils.hash(admin.password)
    admin.password = hashed_password
    new_admin = models.Admin(**admin.dict())
    new_user = models.User(email=admin.email, password=admin.password)
    db.add(new_admin)
    db.add(new_user)
    db.commit()

@router.delete("/{id}", status_code=204)
def delete_admin(id=id,election_id:int = Form(), user:schemas.TokenData=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    election = db.query(models.Election).filter(models.Election.creator_id == int(user.id),
                                                 models.Election.id == election_id)
    if not election:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only election creators can create admins")
    admin_query = db.query(models.Admin).filter(models.Admin.id == id)
    if not admin_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="admin not found")
    admin_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)