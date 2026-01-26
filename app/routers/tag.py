from fastapi import  APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session
from app.database import db_dep
from app.models import Tag
from app.schemas import TagCreateRequest, TagListResponse
from app.utils import generate_slug


router = APIRouter(prefix="/tag", tags=["Tags"])

@router.get("/")
async def get_tag(session:db_dep):

    stmt = select(Tag).order_by(Tag.name)

    res = session.execute(stmt)
    return res.scalars().all()


@router.post("/create")
async def create_tag(session:db_dep, create_data : TagCreateRequest):
    tag = Tag(
    name = create_data.name,
    slug = generate_slug(create_data.name)
    )
    
    session.add(tag)
    session.commit()
    session.refresh(tag)

    return tag


@router.put("update")
async def update_tag(session:db_dep, name:str):
    
    stmt = select(Tag).where(Tag.name == name )
    res = session.execute(stmt)
    tag = res.scalars().first()


    if not stmt:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    session.commit()
    session.refresh(tag)

    return tag


@router.delete("/delete", status_code=204)
async def delete_tag(session:db_dep, tag_id : int):
    stmt = select(Tag).where(Tag.id == tag_id)
    res = session.execute(stmt)

    tag = res.scalars().first()

    if not tag_id:
        raise HTTPException(status_code=404, detail="Tag not found")
    

    session.delete(tag)
    session.commit()