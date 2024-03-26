from fastapi_users import schemas
from pydantic import BaseModel
from typing import Optional, List


class LinksCreate(BaseModel):
    link: str


class ProfilesCreate(BaseModel):
    image_urls: str


class UserBase(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(schemas.BaseUserCreate, UserBase):
    pass


class UserUpdate(schemas.BaseUserUpdate, UserBase):
    pass


class UserRead(schemas.BaseUser, UserBase):

    class Config:
        from_attributes = True


class SoundCreate(BaseModel):
    name: str
    sound_url: str


class SoundRead(SoundCreate):
    id: int
    authors: "UserBase"

    class Config:
        from_attributes = True


class SoundUpdate(SoundCreate):
    name: Optional[str] = None
    sound_url: Optional[str] = None



class CurrentUser(UserRead):
    sounds: Optional[List["SoundCreate"]] = None
    profiles: Optional[List["ProfilesCreate"]] = None
    links: List["LinksCreate"]
