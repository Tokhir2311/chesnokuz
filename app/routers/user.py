from fastapi import APIRouter , HTTPException
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session
from app.models import Users
from app.database import db_dep
from app.schemas import UserCreateRequest, UserListResponse, UserUpdateRequest

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/", response_model=list[UserListResponse])
async def get_users(session:db_dep):
    stmt = select(Users).order_by(Users.name)
    res = session.execute(stmt) 
    
    return res.scalars().all()

    
@router.post("/create")
async def create_user():
    pass

@router.put("/update")
async def update_user():
    pass

@router.delete("/delete", status_code=204)
async def delete_user():
    pass    


