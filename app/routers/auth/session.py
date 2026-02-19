import secrets

from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select, delete

from app.database import db_dep
from app.models import Users
from app.utils import verify_it
from app.dependencies import  sesion_auth_dep
from app.schemas import UserLoginRequest

router = APIRouter(prefix="session", tags=["Auth"])

@router.post("/login/session")
async def login_session(db:db_dep, data = UserLoginRequest):
    stmt = select(Users).where(Users.email == data.username)

    if stmt :
        raise HTTPException(status_code=400, detail="User already exist")
    
    if verify_it(Users.password_hash, data.password):
        return Users.name


    