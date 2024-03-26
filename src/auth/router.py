from fastapi import APIRouter, Depends, File, UploadFile
from fastapi_users import FastAPIUsers
from .models import User, Links, Profiles
from .manager import get_user_manager
from .backend import auth_backend
from src.config import (
    UserRead,
    UserCreate,
    UserUpdate,
    CurrentUser,
    LinksCreate, ProfilesCreate
)
from src.config.crud import Service, upload_file
from .crud.dependencies import user_service, profiles_service, links_service
from .crud.service import UserService
from typing import Annotated, List

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)
current_super_user = fastapi_users.current_user(active=True, superuser=True)

router = APIRouter(
    prefix="/account",
    tags=["account"]
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt"
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth"
)


@router.get(
    "/get/me/current/user/",
    response_model=CurrentUser
)
async def get_current_user(
        service: Annotated[UserService, Depends(user_service)],
        user: User = Depends(current_user)
):
    user = await service.find_one_3_joined(
        join=User.sounds,
        join2=User.profiles,
        join3=User.links,
        pk=user.id
    )
    return user


@router.delete("/delete/mine/account/")
async def delete_account(
        service: Annotated[UserService, Depends(user_service)],
        user: User = Depends(current_user)
):
    return await service.delete_one(pk=user.id)


@router.patch(
    "/update/current/user/me/",
    response_model=UserRead
)
async def edit_me(
        schemas: UserUpdate,
        service: Annotated[UserService, Depends(user_service)],
        user: User = Depends(current_user),
):
    result = await service.edit_one(
        pk=user.id,
        join=User.links,
        schemas=schemas,
        partial=True
    )
    return result


@router.patch("/update/links/")
async def update_links(
        pk: int,
        service: Annotated[Service, Depends(links_service)],
        schemas: LinksCreate
):
    links = await service.edit_one(
        schemas=schemas, pk=pk, join=Links.user
    )
    return links


@router.delete("/delete/links/{pk}/")
async def delete_links(
        pk: int,
        service: Annotated[Service, Depends(links_service)]
):
    return await service.delete_one(pk=pk)


@router.post("/add/new/link/")
async def add_new_lenk(
        schemas: LinksCreate,
        service: Annotated[Service, Depends(links_service)],
        user: User = Depends(current_user)
):
    new_link = Links(
        link=schemas.link,
        user_id=user.id
    )
    result = await service.add_one(new_link)
    return result


@router.post("/upload/file")
async def upload_images(
        file: UploadFile = File(),
        user: User = Depends(current_user)
):
    return await upload_file(file=file, location="account")


@router.post("/add/new/profile/")
async def add_new_images(
        schemas: ProfilesCreate,
        service: Annotated[Service, Depends(profiles_service)],
        user: User = Depends(current_user)
):
    new_link = Profiles(
        image_urls=schemas.image_urls,
        user_id=user.id
    )
    result = await service.add_one(new_link)
    return result


@router.delete("/delete/old/profiles/{pk}/")
async def delete_profiles(
        pk: int,
        service: Annotated[Service, Depends(profiles_service)]
):
    return await service.delete_one(pk=pk)


@router.get(
    "/get/all/users/",
    response_model=List[CurrentUser]
)
async def get_all_users(
        service: Annotated[UserService, Depends(user_service)],
        user: User = Depends(current_super_user)
):
    users = await service.find_all_3_joined(
        join=User.sounds,
        join2=User.profiles,
        join3=User.links,
    )
    print(f"{user.username} selected all users")
    return users
