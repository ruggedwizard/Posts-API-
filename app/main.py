from typing import Optional
from fastapi import FastAPI, Response,status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine,get_db
models.Base.metadata.create_all(bind=engine)
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()



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

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# my_posts= [{"title":"title post 1","content":"content post 1", "id":1}, 
#            {"title":"Final Year Plans","content":"Beat the VC","id":2}]
@app.get("/")
async def root():
    return {"message":"welcome to my api"}

@app.get("/sqlalchemy")
async def test_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {"return": posts}

@app.get("/posts")
async def get_post(db:Session = Depends(get_db)):
    # fetch with regular SQL Query
    # cusor.execute(""" SELECT * FROM posts""")
    # posts=cusor.fetchall()
    # ----------------------------
    # Fetch with SQL Alchemy ORM 
    posts = db.query(models.Post).all()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post:schemas.Post, db:Session=Depends(get_db)):
    # Perfroms operation with plain SQL Query 
    # cusor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # new_post = cusor.fetchone()
    # conn.commit()
    # --------------
    # working with ORM SQL Alchemy
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data":new_post}



@app.get("/posts/{id}")
async def get_post(id:int, db:Session=Depends(get_db)):
    # Regular SQL Command
    # cusor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post=cusor.fetchone()
    # ----------
    # working with SQL ALchemy ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()  

    if not post:
       raise HTTPException(
           status_code= status.HTTP_404_NOT_FOUND,
           detail=f"post with the id of {id} not found"
       )
    return {"data":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db:Session=Depends(get_db)):
    # Delete with Plain SQL Command
    # cusor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,str(id))
    # deleted_post= cusor.fetchone()
    # conn.commit()
    # -------------
    # Delete with SQL Alchemy ORM 
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id:{id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_posts(id:int, updated_post:schemas.Post, db:Session=Depends(get_db)):
    # Updating With Regular SQL function
    # cusor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s  WHERE id=%s RETURNING * """,(post.title, post.content, post.published,str(id)))
    # updated_post = cusor.fetchone()
    # conn.commit()
    # ----------
    # Updating with SQL Alchemy ORM
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id:{id} does not exist")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return {"data":post_query.first()}
