from fastapi import APIRouter, Depends, UploadFile, File
from .crud import sound_service
from .models import Sound
from typing import Annotated, List
from src.config.crud import Service, upload_file
from src.config import SoundRead, SoundCreate, SoundUpdate
from src.auth.router import current_user
from src.auth import User


router = APIRouter(
    prefix="/sounds",
    tags=["sounds"]
)


@router.get(
    "/get/all/sounds/",
    response_model=List[SoundRead]
)
async def find_all_sounds(
        service: Annotated[Service, Depends(sound_service)]
):
    sounds = await service.find_all_joined(
        join=Sound.authors
    )
    return sounds


@router.get(
    "/get/one/sound/{pk}/",
    response_model=SoundRead
)
async def find_one_sound(
        pk: int,
        service: Annotated[Service, Depends(sound_service)]
):
    sound = await service.find_one_joined(
        pk=pk, join=Sound.authors
    )
    return sound


@router.post("/upload/sound/")
async def upload_sound(file: UploadFile = File(...)):
    return await upload_file(file=file, location="sounds")


@router.post("/add/one/sound/")
async def upload_sound(
        schemas: SoundCreate,
        service: Annotated[Service, Depends(sound_service)],
        user: User = Depends(current_user)
):
    new_sound = Sound(
        name=schemas.name,
        sound_url=schemas.sound_url,
        author_id=user.id
    )
    result = await service.add_one(data=new_sound)
    return result


@router.delete("/delete/sound/{pk}/")
async def delete_sound(
        pk: int,
        service: Annotated[Service, Depends(sound_service)]
):
    return await service.delete_one(pk=pk)


@router.patch(
    "/update/one/sound/{pk}/",
    response_model=SoundRead
)
async def update_sound(
        pk: int,
        schemas: SoundUpdate,
        service: Annotated[Service, Depends(sound_service)],
        user: User = Depends(current_user)
):
    edit_sound = await service.edit_one(
        pk=pk, schemas=schemas, join=Sound.authors, partial=True
    )
    return edit_sound
