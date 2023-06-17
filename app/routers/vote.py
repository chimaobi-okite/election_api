from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db
from app import utils


router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)

@router.post("/", status_code=201)
def vote(vote:schemas.Vote, user:schemas.TokenData=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == int(user.id)).first()
    is_admin = db.query(models.Admin).filter(models.Admin.username == user.username,
                                             models.Admin.election_id == vote.election_id).first()
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannt vote from here")
    #check if voter is registered
    voter = db.query(models.Voter).filter(models.Voter.reg_num == vote.reg_num, models.Voter.election_id == vote.election_id).first()
    if not voter:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a registered voter")
    #check if voter has already voted earlier for same post
    has_voted = db.query(models.Vote).filter(models.Vote.election_id == vote.election_id,
                                 models.Vote.post_id == vote.post_id,models.Vote.voter_id == voter.id).first()
    if has_voted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user has voted before")
    new_vote_dict = vote.dict()
    del new_vote_dict["reg_num"]
    print(new_vote_dict)
    new_vote = models.Vote(**new_vote_dict, voter_id = voter.id)
    db.add(new_vote)
    db.commit()

    return Response(status_code=status.HTTP_201_CREATED, content="Success!")