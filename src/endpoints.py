from typing import Annotated

from fastapi import (
    UploadFile,
    Depends,
    Form,
    BackgroundTasks,
    HTTPException,
    status,
    APIRouter,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from db import get_session
import crud
import service

router = APIRouter()


@router.post("/upload-picture", status_code=status.HTTP_201_CREATED)
async def upload_picture(
    file: UploadFile,
    width: Annotated[int, Form()],
    height: Annotated[int, Form()],
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    extention = file.filename.split(".")[1]
    picture_uuid = crud.create_picture(session, extention)
    service.save_picture(picture_uuid, width, height, file, background_tasks, session)
    return {"uuid": picture_uuid}


@router.get(
    "/download-picture", description="Test uuid 899e1802-93ad-42ba-a6ec-b8ef19d347c6"
)
async def download_picture(uuid: str, session: Session = Depends(get_session)):
    picture = crud.get_picture_by_uuid(uuid, session)
    if not picture:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if not picture.processed:
        raise HTTPException(status.HTTP_202_ACCEPTED)
    crud.update_picture_is_downloaded_by_uuid(uuid, session)
    return FileResponse(f"media/{uuid}-resized.{picture.extention}")


@router.get("/statistic")
async def statistic(session: Session = Depends(get_session)):
    pictures = crud.get_all_pictures(session)
    downloaded_qty = 0
    resized_qty = 0
    processing_qty = 0
    for picture in pictures:
        downloaded_qty += picture.downloaded_qty
        if picture.processed:
            resized_qty += 1
        else:
            processing_qty += 1
    return {
        "downloaded_qty": downloaded_qty,
        "resized_qty": resized_qty,
        "processing_qty": processing_qty,
    }
