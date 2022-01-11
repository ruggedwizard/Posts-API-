from typing import Optional
from fastapi import FastAPI, Response,status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from . import models
from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



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

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts= [{"title":"title post 1","content":"content post 1", "id":1}, 
           {"title":"Final Year Plans","content":"Beat the VC","id":2}]
@app.get("/")
async def root():
    return {"message":"welcome to my api"}

@app.get("/posts")
async def get_post():
    cusor.execute(""" SELECT * FROM posts""")
    posts=cusor.fetchall()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post:Post):
    cusor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    new_post = cusor.fetchone()
    conn.commit()
    return {"data":new_post}


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

@app.get("/posts/{id}")
async def get_post(id:int):
    cusor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id)))
    post=cusor.fetchone()
    post = find_post(id)
    if not post:
       raise HTTPException(
           status_code= status.HTTP_404_NOT_FOUND,
           detail=f"post with the id of {id} not found"
       )
    return {"data":post}

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    cusor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,str(id))
    deleted_post= cusor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id:{id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_posts(id:int, post:Post):
    cusor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s  WHERE id=%s RETURNING * """,(post.title, post.content, post.published,str(id)))
    updated_post = cusor.fetchone()
    conn.commit()
    
    if update_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id:{id} does not exist")
    
    return {"data":updated_post}
