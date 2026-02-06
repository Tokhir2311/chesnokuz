from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Cookie, Response
from sqlalchemy import select, desc
from sqlalchemy.orm import Session, sessionmaker, session
from app.models import Post, Category, Users
from app.database import db_dep
from app.schemas import PostListResponse, PostCreateRequest, PostUpdateRequest
from app.utils import generate_slug
from enum import Enum 
router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/")
async def cooke(response: Response):
    response.set_cookie(key="it is key", value="it is value")
    return{"message": "cookie is here"}




@router.get("/", response_model=list[PostListResponse])
async def get_posts(session: db_dep, is_active: bool = None,):
    stmt = select(Post)

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    stmt = stmt.order_by(Post.created_at.desc())
    res = session.execute(stmt)
    return res.scalars().all()




@router.get("/title", response_model=list[PostListResponse])
async def getByname(session : db_dep, title:str):
    stmt = select(Post).where(Post.title.ilike(f"%{title}%"))
    res = session.execute(stmt)

    return res.scalars().all()




@router.post("/create", response_model=PostListResponse)
async def post_create( session: db_dep , 
    create_data: PostCreateRequest):

    post = Post(
        title = create_data.title,
        body = create_data.body,
        slug=generate_slug(create_data.title),
        category_id = create_data.category_id,
        views_cnt = create_data.views_cnt,
        likes_cnt = create_data.likes_cnt,
        comments_cnt = create_data.comments_cnt,
        is_active = create_data.is_active,
        user_id = create_data.user_id
    )

    session.add(post)
    session.commit()
    session.refresh(post)

    return post



@router.put("/update")
async def put( session : db_dep,post_id : int,  update_data : PostUpdateRequest):
    

    stmt = select(Post).where (Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post :
        raise HTTPException(status_code=404, detail="post not found")
    
    if post.title :
        post.title = update_data.title
        post.slug = generate_slug(update_data.title)

    if update_data.body :
        post.body = update_data.body

    if update_data.is_active :
        post.is_active = update_data.is_active

    session.commit()
    session.refresh(post)

    return post



@router.get("{slug}/", response_model=PostListResponse)
async def get_post(session: db_dep, slug: str ):
    stmt = select(Post).where(Post.slug.like(f"%{slug}%"))
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post



@router.delete("/del", status_code=204)
async def delete(session : db_dep, post_id : int):
    
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalars().first()


    if not post_id :
        raise HTTPException(status_code=404, detail="Page not found")


    session.delete(post)
    session.commit()



@router.get("/trends", response_model=list[PostListResponse])
async def get_trend_posts(session:db_dep, limit:int =10):

    weekly = datetime.now() - timedelta(days=7)

    stmt = select(Post).where(Post.created_at >=weekly).order_by(desc(Post.views_cnt)).limit(limit)
    res = session.execute(stmt)

    trends = res.scalars().all()

    return trends



# FILTERS

class by_cat(str, Enum):
    Jahon = "Jahon"
    Sport = "Sport"
    Ilmiy = "Ilmiy"
    Ijtimoiy = "Ijtimoiy"
    Siyosiy = "Siyosiy"


@router.get("/{categ}/", response_model=list[PostListResponse])
async def get_bycat(categ:by_cat, session: db_dep):
    stmt1 = select(Category.id).where(Category.name == categ)
    stmt = select(Post).where(Post.category_id == stmt1) 

    res = session.execute(stmt)
    return res.scalars().all()
    

@router.get("/{user}", response_model=list[PostListResponse])
async def get_byuser(session: db_dep, user: str):
    stmtx = select(Users.id).where(Users.name.ilike(f"%{user}"))      #.ilike(f"%{query}%")
    stmt = select(Post).where(Post.user_id == stmtx)
    res = session.execute(stmt)

    return res.scalars().all()


# @router.get("/{tag}", response_model=list[PostListResponse])
# async def get_bytag(session : db_dep, tag: str):
#     stmt = select(Post).where(Post.tag_id == tag) 
