from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app import oauth2
from .. import models, schemas, oauth2
from .. database import get_db
router = APIRouter()


@router.get("/posts",response_model=List[schemas.Post])
async def get_post(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post("/posts", response_model=schemas.Post ,status_code=status.HTTP_201_CREATED)
async def create_post(post:schemas.PostCreate, db:Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



@router.get("/posts/{id}",response_model=schemas.Post)
async def get_post(id:int, db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()  

    if not post:
       raise HTTPException(
           status_code= status.HTTP_404_NOT_FOUND,
           detail=f"post with the id of {id} not found"
       )
    
    if post.owner_id !=oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not Permited to take such action")
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db:Session=Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id:{id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schemas.Post)
async def update_posts(id:int, updated_post:schemas.PostCreate, db:Session=Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id:{id} does not exist")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
