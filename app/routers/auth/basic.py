from typing import Annotated

from fastapi import HTTPException, APIRouter , Depends
from fastapi.security import HTTPBasicCredentials
from sqlalchemy import select 

from app.database import db_dep
from app.models import Users 
from app.schemas import  UserUpdateRequest 
from app.dependencies import basic_auth_dep, basic_cur_user_get

router = APIRouter(prefix="/basic", tags=["/Auth"])

@router.get("/profile")
async def login(db:db_dep, current_user:basic_auth_dep):
    
    if not current_user:
        raise HTTPException(status_code=404, detail="not found")

    return current_user
        


@router.put("/update")
async def update_user(db:db_dep, current_user:basic_auth_dep, data:UserUpdateRequest):
    for attr, value in data.model_dump(exclude_unset=True).items():
        setattr(current_user, attr, value)

    db.commit()
    db.refresh(current_user)

    return current_user()  


# @router.delete("/delete", status_code=204)
# async def delete_profile(db:db_dep, current_user:basic_auth_dep):
#     current_user.username = None,
#     current_user.is_active = False,
#     current_user.is_deleted = True

#     db.commit()