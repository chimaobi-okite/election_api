from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id : int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None

class ElectionCreate(BaseModel):
    title: str

class ElectionUpdate(ElectionCreate):
    is_active: bool
    is_finished: bool

class ElectionOut(ElectionUpdate):
    id : int

    class Config:
        orm_mode = True

class Admin(UserCreate):
    election_id:int
    is_super:bool = False

class Post(BaseModel):
    post : str
    election_id: int

class PostOut(Post):
    id:int

    class Config:
        orm_mode = True

class Participant(BaseModel):
    name:str
    post_id:int
    election_id:int

class ParticipantOut(Participant):
    id:int 
    photo_url:Optional[str] = None

    class Config:
        orm_mode = True

class Vote(BaseModel):
    reg_num:int
    post_id:int
    participant_id:int
    election_id:int

class VoteOut(BaseModel):
    id:int
    post_id:int
    participant_id:int
    election_id:int

    class Config:
        orm_mode = True

class PartOutResult(ParticipantOut):
    votes:Optional[List[VoteOut]] = None
    total_votes:Optional[int] = None

    class Config:
        orm_mode = True


class PostPartResults(PostOut):
    participants : Optional[List[PartOutResult]] = None

    class Config:
        orm_mode = True

class PostParticipants(PostOut):
    participants : Optional[List[ParticipantOut]] = None

class ElectionParticipants(ElectionOut):
    posts: Optional[List[PostPartResults]] = None
    

    class Config:
        orm_mode = True

class ElectionResults(ElectionOut):
    posts: Optional[List[PostPartResults]] = None

    class Config:
        orm_mode = True

class VotersCount(BaseModel):
    count: int

    class Config:
        orm_mode = True
