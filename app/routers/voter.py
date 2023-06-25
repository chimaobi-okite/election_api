import codecs
import csv
from fastapi import FastAPI, Form, Response, UploadFile, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db
from app import utils

router = APIRouter(
    prefix="/voters",
    tags=['Voters']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def register_voters(file: UploadFile, election_id:str = Form(), level:int = Form(),
                           department:str = Form(), 
                           db:Session = Depends(get_db), user:schemas.TokenData = Depends(oauth2.get_current_user)):
    election = db.query(models.Election).filter(
        models.Election.id == election_id, models.Election.creator_id == str(user.id)).first()
    if not election:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    is_registered_query = db.query(models.Voter).filter(models.Voter.election_id == election_id,
                                                   models.Voter.department == department, models.Voter.level == level)
    if is_registered_query.first():
        is_registered_query.delete(synchronize_session=False)
        db.commit()
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    enrollments = []
    fields = csvReader.fieldnames
    if "NAMES" not in fields or "REG. NO." not in fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="either Names field or REG. NO. not in file")
    for rows in csvReader:             
        new_data = {"name":rows['NAMES'], "reg_num":rows['REG. NO.'],
                    "level":level, "department":department, "election_id":election_id}
        enrollment = models.Voter(**new_data)
        enrollments.append(enrollment)
    
    file.file.close()
    db.add_all(enrollments)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED, content="Voters registered successfuly")
     