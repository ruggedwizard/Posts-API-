from fastapi import FastAPI, APIRouter
from app import models
from .database import engine
from passlib.context import CryptContext
from app.routers import post, user, auth
from app.config import settings
models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()




router = APIRouter()
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message":"welcome to my api"}