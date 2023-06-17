import os
import shutil
from fastapi import FastAPI, File, Form, Response, status, HTTPException, Depends, APIRouter, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db
from app import utils, config


router = APIRouter(
    prefix="/participants",
    tags=['Participants']
)

@router.post("/", response_model=schemas.ParticipantOut, status_code=201)
def add_participant(participant: schemas.Participant,
                    user:schemas.TokenData=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    if not db.query(models.Election).join(
        models.Post, models.Election.id == models.Post.election_id).filter(models.Election.id == participant.election_id,
                                        models.Election.creator_id == int(user.id), models.Post.id == participant.post_id).first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    new_participant = models.Participant(**participant.dict())
    db.add(new_participant)
    db.commit()
    db.refresh(new_participant)

    return new_participant

@router.put("{id}/photo", status_code=201)
async def upload_photo(id:int, file: UploadFile = File(...),
                       user:schemas.TokenData=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
        participant_query = db.query(models.Participant).filter(models.Participant.id == id)
        participant = participant_query.first()
        if not participant:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="participant with {id} not found")
        if not db.query(models.Election).join(models.Participant,
                                    models.Election.id == models.Participant.election_id).filter(
             models.Election.creator_id == int(user.id), models.Participant.id == id).first():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        photo_loc = os.path.join(config.PHOTO_DIR, str(participant.id))
        with open(f'{photo_loc}','wb') as image:
            image.write(file.file.read())
            image.close()
        participant_query.update({"photo_url":photo_loc}, synchronize_session=False)
        db.commit()
        db.refresh(participant_query.first())
        return participant_query.first()

@router.put("/{id}", response_model=schemas.ParticipantOut, status_code=201)
def update_participant(id: int, new_participant: schemas.Participant,
                    user:schemas.TokenData=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    participant_query = db.query(models.Participant).filter(models.Participant.id == id)
    old_participant = participant_query.first()
    if not old_participant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"participant with {id} not found")
    if not db.query(models.Election).join(models.Participant,
                                    models.Election.id == models.Participant.election_id).filter(
             models.Election.creator_id == int(user.id), models.Participant.id == id).first():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    participant_query.update(new_participant.dict(), synchronize_session=False)
    db.commit()
    db.refresh(participant_query.first())
    return participant_query.first()

@router.delete("/{id}", status_code=204)
def delete_admin(id=id, user:schemas.TokenData=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    participant_query = db.query(models.Participant).filter(models.Participant.id == id)
    old_participant = participant_query.first()
    if not old_participant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"participant with {id} not found")
    if not db.query(models.Election).join(models.Participant,
                                    models.Election.id == models.Participant.election_id).filter(
             models.Election.creator_id == int(user.id), models.Participant.id == id).first():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    participant_query.delete(nsynchronize_session=False)
    db.commit()
    db.refresh(participant_query.first())
    return Response(status_code=status.HTTP_204_NO_CONTENT)