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

    post_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("post.id"), primary_key=True)
    media_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("media.id"), primary_key=True)

    def __repr__(self):
        return f"PostMedia({self.post_id} - {self.media_id})"
    

class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    url: Mapped[str] = mapped_column(String(100))
    
    post:Mapped["Post"] = relationship("Post", secondary="post_media", back_populates="media")
   

class Post(BaseModel):
    __tablename__ = "post"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    body: Mapped[str] = mapped_column(Text)
    category_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("category.id"))
    views_cnt: Mapped[int] = mapped_column(BigInteger, default=0)
    likes_cnt: Mapped[int] = mapped_column(BigInteger, default=0)
    comments_cnt: Mapped[int] = mapped_column(BigInteger, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    comments: Mapped["Comment"] = relationship("Comment", back_populates="post")
    tag: Mapped[list["Tag"]] = relationship("Tag", secondary="post_tag", back_populates="posts" )
    category: Mapped["Category"] = relationship("Category", back_populates="post")
    media: Mapped["Media"] = relationship("Media", secondary="post_media", back_populates="post")
    

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
    post_cnt: Mapped[int] = mapped_column(BigInteger, default=0)
    post_view_cnt: Mapped[int] = mapped_column(BigInteger, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=True)

    profession: Mapped["Profession"] = relationship("Profession", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")

    def __repr__(self):
        return {self.name}
    
class Profession(Base):
    __tablename__= "profession"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    user: Mapped[list["Users"]] = relationship("Users", back_populates="profession")

    def __repr__(self):
        return {self.name}
    

class Comment(BaseModel):
    __tablename__ = "comment"

    user_id : Mapped[int] = mapped_column(BigInteger, ForeignKey(Users.id), default=1)
    post_id : Mapped[int] = mapped_column(BigInteger, ForeignKey(Post.id), default=1)
    text : Mapped[str] = mapped_column(Text)
    is_active : Mapped[bool] = mapped_column(Boolean)

    user: Mapped["Users"] = relationship("Users", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def __repr__(self):
        return {self.user_id}, {self.text}


class Tag(Base):
    __tablename__="tag"
    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name:Mapped[str] = mapped_column(String, nullable=False)
    slug:Mapped[str] = mapped_column(String)

    posts:Mapped[list["Post"]] = relationship( secondary="post_tag", back_populates="tag")
    
    def __repr__(self):
        return {self.name}

class PostTag(Base):
    __tablename__ = "post_tag"

    post_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("post.id"), primary_key=True)
    tag_id: Mapped[int]= mapped_column(BigInteger, ForeignKey("tag.id"), primary_key=True)

   

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String)
  
    post: Mapped[list["Post"]] = relationship("Post", back_populates="category")


    def __repr__(self):
        return {self.name}
    

class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    post_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    device_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class Devices(Base):
    __tablename__="devices"

    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_agent: Mapped[str] = mapped_column(String, nullable=False)
    last_active: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now()) 
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())



class User_Search(Base):
    __tablename__ = "user_search"

    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    item: Mapped[str] = mapped_column(String, nullable=False)
    cnt : Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())                 
