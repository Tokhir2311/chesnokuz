from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import session, sessionmaker
from app.database import db_dep 
from app.models import Comment
from app.schemas import CommentCreateRequest, CommentListResponse


router = APIRouter(prefix="/comment", tags=["Comment"])


@router.get("/", response_model=list[CommentListResponse])
async def get_comments():
    comment = select(Comment)
    res = session.execute(comment).scalars().all()
    return res

@router.post("/create")
async def comment_cret(session: db_dep, create_data:CommentCreateRequest):
    comment = Comment(
        user_id = create_data.user_id,
        post_id = create_data.post_id,
        text = create_data.text
    )
    
    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment


@router.delete("{comment_id}", status_code=204)
async def del_comment(session: db_dep, comment_id : int):
    stmt = select(Comment).where(Comment.id == comment_id)
    res = session.execute(stmt)
    comment = res.scalars().first()

    if not comment_id:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    session.delete(comment)
    session.commit()