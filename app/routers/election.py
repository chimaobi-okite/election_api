import json
from fastapi import FastAPI, Form, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder
from pydantic.tools import parse_obj_as

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db
from app import utils


router = APIRouter(
    prefix="/elections",
    tags=['Elections']
)

@router.post("/", response_model=schemas.ElectionOut, status_code=201)
def create_election(election: schemas.ElectionCreate,
                    user:schemas.TokenData=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):


    new_election = models.Election(**election.dict(), creator_id=user.id, is_active=False, is_finished=False)
    db.add(new_election)
    db.commit()
    db.refresh(new_election)

    return new_election

@router.get("/{id}", response_model=schemas.ElectionOut)
def get_election(id:int, db: Session = Depends(get_db)):

    election = db.query(models.Election).filter(models.Election.id == id).first()
    if not election:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="election not found")
    return election

@router.get("/", response_model=List[schemas.ElectionOut])
def get_elections(db : Session = Depends(get_db)):
    elections = db.query(models.Election).all()
    return elections

@router.put("/{id}", response_model=schemas.ElectionOut, status_code=201)
def update_election(id: int, new_election: schemas.ElectionUpdate,
                    user:schemas.TokenData=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    election_query = db.query(models.Election).filter(models.Election.id == id)
    old_election = election_query.first()
    if not old_election:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="election not found")
    if str(old_election.creator_id) != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    election_query.update(new_election.dict(), synchronize_session=False)
    db.commit()
    db.refresh(election_query.first())
    return election_query.first()

@router.delete("/{id}",  status_code=204)
def delete_election(id: int, user:schemas.TokenData=Depends(oauth2.get_current_user),
                     db: Session = Depends(get_db)):

    election_query = db.query(models.Election).filter(models.Election.id == id)
    old_election = election_query.first()
    if not old_election:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="election not found")
    if str(old_election.creator_id) != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    election_query.delete(synchronize_session=False)
    db.commit()
    return 

@router.get("/{id}/participants", response_model=schemas.ElectionParticipants)
def get_participants(id:int, db: Session = Depends(get_db)):
    election = db.query(models.Election).filter(models.Election.id == id).first()
    if not election:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Election With id {id} not found")
    participants = db.query(models.Election).options(
        joinedload(models.Election.posts)).options(
        joinedload(models.Election.posts, models.Post.participants)).filter(
        models.Election.id == id).first()
    return participants

@router.get("/{id}/results",response_model=schemas.ElectionResults) 
def get_election_results(id: int,user:Optional[schemas.TokenData]=Depends(oauth2.get_current_user) ,db: Session = Depends(get_db)):
    election = db.query(models.Election).filter(models.Election.id == id).first()
    if not election:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Election With id {id} not found")
    if not int(user.id) == election.creator_id:
        if not election.is_active and election.is_finished:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    election_results = db.query(models.Election).options(
        joinedload(models.Election.posts)).options(
        joinedload(models.Election.posts, models.Post.participants)).options(joinedload(
        models.Election.posts, models.Post.participants, models.Participant.votes)).filter(
        models.Election.id == id).first()
    results = jsonable_encoder(election_results)
    for i, post in enumerate(results.get('posts')):
        for j, participant in enumerate(post.get('participants')):
            participant['total_votes'] = len(participant['votes'])
            results['posts'][i]['participants'][j]['total_votes'] = len(participant['votes'])
    return results
    

    