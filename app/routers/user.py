
from fastapi import status,Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import get_db

router = APIRouter(
    tags=["Users"]
)

@router.post("/createusers",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user:schemas.User, db:Session=Depends(get_db)):
    # hash the password user.password
    
    # hashed_password = pwd_context.hash(user.password)
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{id}", response_model=schemas.UserOut)
async def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"user with the id: {id} not found")
    return user