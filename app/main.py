from fastapi import FastAPI, APIRouter

from app import models
from .database import engine


import psycopg2
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext
import time
from app.routers import post, user, auth
models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

router = APIRouter()
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(user.router)



while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="admin", cursor_factory=RealDictCursor)
        cusor = conn.cursor()
        print("Database connection Sucessful!!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(6)


@app.get("/")
async def root():
    return {"message":"welcome to my api"}