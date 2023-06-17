from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import user, auth, election, post, participant, voter, vote, admin
# from .config import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(user.router)
app.include_router(auth.router)
app.include_router(election.router)
app.include_router(post.router)
app.include_router(participant.router)
app.include_router(voter.router)
app.include_router(vote.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}