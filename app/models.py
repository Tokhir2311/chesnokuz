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


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    url: Mapped[str] = mapped_column(String(100))


class PostMedia(Base):
    __tablename__ = "post_media"

    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("media.id"), primary_key=True)

    post_id:Mapped["PostMedia"] = relationship("PostMedia", back_populates="Post")
    media_id:Mapped["PostMedia"] = relationship("PostMedia", back_populates="Media")

    def __repr__(self):
        return f"PostMedia({self.post_id} - {self.media_id})"


class Post(BaseModel):
    __tablename__ = "post"

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    body: Mapped[str] = mapped_column(Text)
    category_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("Category.id"))
    views_cnt:Mapped[int] = mapped_column(BigInteger, default=0)
    likes_cnt:Mapped[int] = mapped_column(BigInteger, default=0)
    comments_cnt:Mapped[int] = mapped_column(BigInteger, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    

    category_id:Mapped["Category"] = relationship("Category", back_populates="posts")
    


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

    profession_id : Mapped["Profession"] = relationship("Profession", back_populates="Users")

    def __repr__(self):
        return {self.name}
    
class Profession(Base):
    __tablename__= "profession"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name:Mapped[str] = mapped_column(String(100), nullable=False)

    name:Mapped["Profession"] = relationship("Profession", back_populates="Users")

    def __repr__(self):
        return {self.name}
    

class Comment(BaseModel):
    __tablename__ = "comment"

    user_id : Mapped[int] = mapped_column(BigInteger, ForeignKey(Users.id))
    post_id : Mapped[int] = mapped_column(BigInteger, ForeignKey(Post.id))
    text : Mapped[str] = mapped_column(Text)
    is_active : Mapped[bool] = mapped_column(Boolean)


    user_id:Mapped["Users"] = relationship("Users", back_populates="Comment")
    post_id:Mapped["Post"] = relationship("Post", back_populates="Comment")

    def __repr__(self):
        return {self.user_id}, {self.text}


class Tag(BaseModel):
    __tablename__="tag"
    
    name:Mapped[str] = mapped_column(String, nullable=False)
    slug:Mapped[str] = mapped_column(String)

    def __repr__(self):
        return {self.name}

class PostTag(Base):
    __tablename__ = "post_tag"

    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    post_id:Mapped[int] = mapped_column(BigInteger, ForeignKey(Post.id))
    tag_id:Mapped[int]= mapped_column(BigInteger, ForeignKey(Tag.id))

    post_id:Mapped["PostTag"] = relationship("PostTag", back_populates="Post")
    tag_id:Mapped["PostTag"] = relationship("PostTag", back_populates="Tag")

class Category(Base):
    __tablename__ = "category"

    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name:Mapped[str] = mapped_column(String, nullable=False)
    slug:Mapped[str] = mapped_column(String)

    
    id:Mapped[list["Post"]] = relationship("Post", back_populates="Post")


    def __repr__(self):
        return {self.name}