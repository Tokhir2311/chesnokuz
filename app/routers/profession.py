from fastapi import APIRouter, HTTPException
from sqlalchemy import select 
from sqlalchemy.orm import session
from app.database import db_dep
from app.models import Profession
from app.schemas import ProfessionCreateRequest, ProfessionListResponse 

router = APIRouter(prefix="/profession", tags=["Profession"]) 


@router.get("/professions", response_model=list[ProfessionListResponse])
async def get_profesh(session:db_dep):
    profession = select(Profession)
    res = session.execute(profession).scalars().all()
    
    return res


@router.post("/create")
async def prof_create(session : db_dep, create_data : ProfessionCreateRequest):
    profession = Profession(name = create_data.name)
    session.add(profession)
    session.commit()
    session.refresh(profession)

    return profession



@router.delete("/del", status_code=204)
async def prof_del(session : db_dep, prof_id:int):
    stmt = select(Profession).where(Profession.id == prof_id)
    res = session.execute(stmt)
    prof = res.scalars().first()

    if not prof_id:
        raise HTTPException(status_code=404, detail="Profession not found")
    
    session.delete(prof)
    session.commit()
