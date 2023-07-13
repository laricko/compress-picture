from typing import Annotated

from fastapi import FastAPI
from uvicorn import run

from db import Base, engine
from endpoints import router

Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", reload=True)
