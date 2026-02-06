from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, AliasPath
from typing import List 


class PostCreateRequest(BaseModel):
    title: str
    body: str
    category_id: int | None = None
    views_cnt: int | None = None
    likes_cnt: int | None = None
    comments_cnt: int | None = None
    is_active: bool | None = True
    user_id: int | None = None

class PostListResponse(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    is_active: bool


class PostUpdateRequest(BaseModel):
    title: str | None = None
    body : str | None = None
    is_active : bool | None = None


class CategoryCreateRequest(BaseModel):
    name:str
    

class CategoryListResponse(BaseModel):
    name:str
    slug:str


class UserListResponse(BaseModel):
    email:str
    name:str
    surname:str
    bio:str


class UserCreateRequest(BaseModel):
    profession_id : int
    email: EmailStr
    password_hash:str
    name:str
    surname:str
    bio:str
    is_active: bool | None = None
    is_staff: bool | None = None
    is_superuser : bool | None = None


class UserUpdateRequest(BaseModel):
    email: EmailStr
    password_hash:str
    name:str
    surname:str
    bio:str
    is_active:bool | None = None
    is_stuff: bool | None = None
    is_superuser : bool | None = None

    

class TagUpdateRequest(BaseModel):
    name:str | None = None


class TagCreateRequest  (BaseModel):
    name:str | None = None



class TagListResponse(BaseModel):
    name:str
    slug:str

class ProfessionCreateRequest(BaseModel):
    name : str

class ProfessionListResponse(BaseModel):
    name : str
    id : int



class CommentCreateRequest(BaseModel):
    user_id : int | None = None
    post_id : int | None = None
    text: str

class CommentListResponse(BaseModel):
    user_id : int
    post_id : int
    text: str
    is_active : bool


class WeatherCoord(BaseModel):
    lon: float
    lat: float


class WeatherInline(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class WeatherMainInline(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int 
    humidity: int 
    sea_level: int
    grnd_level: int


class WeatherResponse(BaseModel):
    coord: WeatherCoord
    weather: list[WeatherInline]
    temp: float = Field(validation_alias=AliasPath("main", "temp"))
    humidity: int = Field(validation_alias=AliasPath("main", "humidity"))


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str