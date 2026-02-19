from typing import Annotated
from sqlalchemy import select
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi import Depends, HTTPException

from app.database import db_dep
from app.models import Users
from app.utils import verify_it

basic = HTTPBasic()


basic_auth_dep = Annotated[HTTPBasicCredentials, Depends(basic)]

def get_cur_user(session : db_dep, credentials : basic_auth_dep):
    stmt = select(Users).where(Users.email == credentials.username)
    user = session.execute(stmt).scalars().first()


    if not user:
        raise HTTPException(status_code=404, detail="user not found")   

    if not verify_it(credentials.password, user.password_hash):
        raise HTTPException(status_code=400, detail="wrong password")
    
    return user

basic_cur_user_get = Annotated[Users, Depends(get_cur_user)]