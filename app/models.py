from __future__ import annotations 

from datetime import datetime
from sqlalchemy import BigInteger, String, Boolean, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )



#########################################################

class PostMedia(Base):
    __tablename__ = "post_media"

    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    post_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("post.id"))
    media_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("media.id"))

    post:Mapped["Post"] = relationship(back_populates="postmedia")
    media:Mapped["Media"] = relationship( back_populates="post_media")

    def __repr__(self):
        return f"PostMedia({self.post_id} - {self.media_id})"
    

class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    url: Mapped[str] = mapped_column(String(100))

    post_media:Mapped[list["PostMedia"]] = relationship(back_populates="media")


class Post(BaseModel):
    __tablename__ = "post"

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    body: Mapped[str] = mapped_column(Text)
    category_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("category.id"))
    views_cnt:Mapped[int] = mapped_column(BigInteger, default=0)
    likes_cnt:Mapped[int] = mapped_column(BigInteger, default=0)
    comments_cnt:Mapped[int] = mapped_column(BigInteger, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    postmedia: Mapped[list["PostMedia"]] = relationship(back_populates="post")
    category: Mapped["Category"] = relationship(back_populates="posts")
    commentp: Mapped["Comment"] = relationship(back_populates="postc") 
    post_t_ag: Mapped["PostTag"] = relationship(back_populates="postt")

    def __repr__(self):
        return {self.title}


class Users(BaseModel):
    __tablename__="user"

    profession_id :Mapped[int] = mapped_column(BigInteger, ForeignKey("profession.id"))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(120), nullable=False)
    name : Mapped[str] = mapped_column(String(45), nullable=False)
    surname: Mapped[str] = mapped_column(String(45))
    bio: Mapped[str] = mapped_column(Text)
    post_cnt:Mapped[int] = mapped_column(BigInteger, default=0)
    post_view_cnt:Mapped[int] = mapped_column(BigInteger, default=0)
    is_active:Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_staff:Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_superuser:Mapped[bool] = mapped_column(Boolean, nullable=True)

    profession : Mapped["Profession"] = relationship(back_populates="users")
    comment: Mapped["Comment"] = relationship(back_populates="user")

    def __repr__(self):
        return {self.name}
    
class Profession(Base):
    __tablename__= "profession"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name:Mapped[str] = mapped_column(String(100), nullable=False)

    users: Mapped["Users"] = relationship(back_populates="profession")

    def __repr__(self):
        return {self.name}
    

class Comment(BaseModel):
    __tablename__ = "comment"

    user_id : Mapped[int] = mapped_column(BigInteger, ForeignKey(Users.id))
    post_id : Mapped[int] = mapped_column(BigInteger, ForeignKey(Post.id))
    text : Mapped[str] = mapped_column(Text)
    is_active : Mapped[bool] = mapped_column(Boolean)


    user: Mapped[list["Users"]] = relationship(back_populates="comment")
    postc: Mapped["Post"] = relationship(back_populates="commentp")

    def __repr__(self):
        return {self.user_id}, {self.text}


class Tag(BaseModel):
    __tablename__="tag"
    
    name:Mapped[str] = mapped_column(String, nullable=False)
    slug:Mapped[str] = mapped_column(String)

    posttag: Mapped[list["PostTag"]] = relationship(back_populates="tag")
    
    def __repr__(self):
        return {self.name}

class PostTag(Base):
    __tablename__ = "post_tag"

    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    post_id:Mapped[int] = mapped_column(BigInteger, ForeignKey(Post.id))
    tag_id:Mapped[int]= mapped_column(BigInteger, ForeignKey(Tag.id))

    postt: Mapped["Post"] = relationship(back_populates="post_t_ag")
    tag: Mapped["Tag"] = relationship(back_populates="posttag")


class Category(Base):
    __tablename__ = "category"

    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name:Mapped[str] = mapped_column(String, nullable=False)
    slug:Mapped[str] = mapped_column(String)


    posts:Mapped[list["Post"]] = relationship(back_populates="category")


    def __repr__(self):
        return {self.name}