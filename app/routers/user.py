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

    
@router.post("/create", response_model=list[UserListResponse])
async def create_user(session:db_dep, create_data:UserCreateRequest):
    user = Users(
        profession_id = create_data.profession_id,
        email = create_data.email,
        password_hash = create_data.password_hash,      #utils
        name = create_data.name,
        surname = create_data.surname,
        bio = create_data.bio,
        is_active = create_data.is_active,
        is_staff = create_data.is_staff,
        is_superuser = create_data.is_superuser
    )

    res = session.add(user)
    session.commit()
    session.refresh(user)

    return res

@router.put("/update")
async def update_user(session:db_dep, user_id : int, update_data:UserUpdateRequest):

    stmt = select(Users).where(Users.id == user_id)
    res = session.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="Not found")

    user.email = update_data.email
    user.password_hash = update_data.password_hash
    user.name = update_data.name
    user.surname = update_data.surname
    user.bio = update_data.bio 
    user.is_activen = update_data.is_active




@router.delete("/delete", status_code=204)
async def delete_user(session:db_dep, user_id:int):

    stmt = select(Users).where(Users.id == user_id)
    res = session.execute(stmt) 
    user = res.scalars().first()

    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    

    session.delete(user)
    session.commit()
