from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)

class Election(Base):
    __tablename__ = "elections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    is_finished = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    posts = relationship("Post", backref="election")
    participants = relationship("Participant", backref="election")
    

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    election_id = Column(Integer, ForeignKey("elections.id", ondelete="CASCADE"), nullable=False) 
    is_super =  Column(Boolean, nullable=False, server_default="False")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    post = Column(String, nullable=False)
    election_id = Column(Integer, ForeignKey("elections.id", ondelete="CASCADE"), nullable=False)

    participants = relationship("Participant", backref="post")

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    photo_url = Column(String, unique=True, nullable=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    election_id = Column(Integer, ForeignKey("elections.id", ondelete="CASCADE"), nullable=False)

    votes = relationship("Vote", backref="participant")

class Voter(Base):

    __tablename__ = "voters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    reg_num = Column(BigInteger, nullable=False)
    level = Column(Integer, nullable=False)
    department = Column(String, nullable=False)
    election_id = Column(Integer, ForeignKey("elections.id", ondelete="CASCADE"), nullable=False)

class Vote(Base):

    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("voters.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participants.id", ondelete="CASCADE"), nullable=False)
    election_id = Column(Integer, ForeignKey("elections.id", ondelete="CASCADE"), nullable=False)