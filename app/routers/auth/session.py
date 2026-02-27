import secrets
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select, delete

from app.database import db_dep
from app.models import Users, User_session_token
from app.utils import verify_it
from app.dependencies import  session_auth_dep
from app.schemas import UserLoginRequest, UserListResponse
from app.config import settings

router = APIRouter(prefix="/session", tags=["Auth"])

@router.post("/login")
async def login_session(db:db_dep, data: UserLoginRequest, response: Response):
    stmt = select(Users).where(Users.email == data.username)
    res = db.execute(stmt)
    user = res.scalars().first()

    if not user :
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_it(data.password, Users.password_hash):
        return HTTPException(status_code=401, detail="Username or password wrong")
    
    sessionId = secrets.token_urlsafe(32) 

    stmt = delete(User_session_token).where(User_session_token.user_id == user.id)
    db.execute(stmt)
    db.flush()


    new_session = User_session_token(
        token = sessionId,
        user_id=user.id,
        expires_at = datetime.now(tz=timezone.utc) 
        + timedelta(days=settings.SESSION_ID_EXPIRE_DAYS), )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    response.set_cookie(
        key = "session_id",
        value= sessionId,
        httponly=True,
        secure=True,  # HTTPS
        samesite="strict",
        max_age=settings.SESSION_ID_EXPIRE_DAYS * 24 * 60 * 60,
    )


@router.get("/profile", response_model=UserListResponse)
async def user_profile(session : db_dep, current_user: session_auth_dep):
    return current_user

    