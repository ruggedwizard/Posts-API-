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

# @app.get("/posts", response_model=List[schemas.Post])
# async def get_post(db:Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts

# @app.post("/posts", response_model=schemas.Post ,status_code=status.HTTP_201_CREATED)
# async def create_post(post:schemas.PostCreate, db:Session=Depends(get_db)):
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post



# @app.get("/posts/{id}",response_model=schemas.Post)
# async def get_post(id:int, db:Session=Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()  

#     if not post:
#        raise HTTPException(
#            status_code= status.HTTP_404_NOT_FOUND,
#            detail=f"post with the id of {id} not found"
#        )
#     return post


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id:int,db:Session=Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id)
#     if post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id:{id} does not exist")
    
#     post.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}", response_model=schemas.Post)
# async def update_posts(id:int, updated_post:schemas.PostCreate, db:Session=Depends(get_db)):
#     post_query=db.query(models.Post).filter(models.Post.id==id)
#     post = post_query.first()
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id:{id} does not exist")
    
#     post_query.update(updated_post.dict(),synchronize_session=False)
#     db.commit()
#     return post_query.first()

# @app.post("/createusers",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# async def create_user(user:schemas.User, db:Session=Depends(get_db)):
#     # hash the password user.password
    
#     # hashed_password = pwd_context.hash(user.password)
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get("/users/{id}", response_model=schemas.UserOut)
# async def get_user(id:int, db:Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#         detail=f"user with the id: {id} not found")
#     return user