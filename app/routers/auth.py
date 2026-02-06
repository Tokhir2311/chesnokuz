from typing import Annotated

from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select 

from app.database import db_dep
from app.models import Users 
from app.schemas import UserRegisterRequest
from app.utils import hash_it, verify_it

basic= HTTPBasic()

router = APIRouter(prefix='/auth', tags=["Authorization"])

@router.post("/register")
async def register(db:db_dep, data: UserRegisterRequest):
    stmt =  select(Users).where(Users.email == data.email)
    res = db.execute(stmt).scalars().first()

    if res:
        raise HTTPException(status_code=400, detail="user already exist")
    

    # res2 = verify_it(data.password)


    # if res2:
        
    user = Users(
        email = data.email,
        password_hash = hash_it(data.password)
        )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    
    # else : 
    #     raise 
