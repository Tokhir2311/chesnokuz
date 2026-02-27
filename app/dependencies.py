from datetime import datetime, timezone
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi import Depends, HTTPException, Request

from app.database import db_dep
from app.models import Users, User_session_token
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


def get_current_user_session(session:db_dep, request: Request):
    sessionId = request.cookies.get("session_id")
    
    if not sessionId:
        raise HTTPException(status_code=401, detail="Not authentificated")

    stmt = select(User_session_token).where(User_session_token.token==sessionId)
    session_obj = session.execute(stmt).scalars().first()

    if not session_obj:
        raise HTTPException(status_code=401, detail="Not authentificated")
    
    if session_obj.expires_at<datetime.now(tz=timezone.utc):
        session.delete(session_obj)
        session.commit()
        raise HTTPException(status_code=401, detail="Not autheticated")
    
    stmt=(select(Users)
    .where(Users.id==session_obj.user_id)
    .options(joinedload(Users.professions))
    )
    user = session.execute(stmt).scalars().first()

    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="not found")
    
    return user

session_auth_dep = Annotated[Users, Depends(get_current_user_session)]