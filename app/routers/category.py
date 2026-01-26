from fastapi  import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session
from app.database import db_dep
from app.models import Category
from app.schemas import CategoryCreateRequest, CategoryListResponse
from app.utils import generate_slug


router = APIRouter(prefix="/category", tags=["Category"])


@router.get("/", response_model=list[CategoryListResponse])
async def get_cats(session :db_dep):
    stmt = select(Category)

    stmt = stmt.order_by(Category.name.asc())

    res = session.execute(stmt)
    
    return res.scalars().all()


@router.post("/create")
async def create_cat(session:db_dep, create_data : CategoryCreateRequest):
    category = Category(
        name = create_data.name,
        slug = generate_slug(create_data.title)
    )

    session.add(category)
    session.commit()
    session.refresh(category)

    return category


@router.put("/update")
async def update(session : db_dep, category_id:int, update_data: CategoryCreateRequest):

    stmt = select(Category).where(Category.id == category_id)
    res = session.execute(stmt)
    cat = res.scalars().first()

    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if cat.name:
        cat.name = update_data.name 

    session.commit()
    session.refresh(cat)

    return cat



@router.delete("/delete", status_code=204)
async def delete_cat(session : db_dep, category_id:int):
    stmt = select(Category).where(Category.id == category_id)
    res = session.execute(stmt)
    cat = res.scalars().first()

    if not category_id :
        raise HTTPException(status_code=404, detail="Category not found")
    


    session.delete(cat)
    session.commit()