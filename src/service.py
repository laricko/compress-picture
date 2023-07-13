from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi import UploadFile, BackgroundTasks, HTTPException, status
from PIL import Image

from db import Picture
from config import settings


def save_picture(
    uuid: str,
    width: int,
    height: int,
    file: UploadFile,
    worker: BackgroundTasks,
    session: Session,
) -> None:
    extention = file.filename.split(".")[1]
    file_location = f"media/{uuid}.{extention}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    if len(worker.tasks) >= settings.resizing_tasks_allowed_amount:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "too many pictures are processing now, try again later",
        )
    worker.add_task(resize_picture, file_location, width, height, session, uuid)


def resize_picture(
    file_location: str, width: int, height: int, session: Session, uuid
) -> None:
    file_location_without_extention, extention = file_location.split(".")
    image = Image.open(file_location)
    image.thumbnail((width, height))
    image.save(f"{file_location_without_extention}-resized.{extention}")
    update_picture_resized(uuid, session)


def update_picture_resized(uuid: str, session: Session) -> None:
    query = update(Picture).where(Picture.uuid == uuid).values(processed=datetime.now())
    session.execute(query)
    session.commit()
