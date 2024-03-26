from fastapi import UploadFile
import aiofiles
import uuid
import os


async def upload_file(
    file: UploadFile,
    location: str
):
    file_name = f"{str(uuid.uuid4())}_{file.filename}"
    file_location = f"media/{location}/{file_name}"
    async with aiofiles.open(file_location, "wb") as finished:
        while content := await file.read(92160):
            await finished.write(content)
    return file_location
