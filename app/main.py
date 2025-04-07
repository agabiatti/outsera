from fastapi import FastAPI
from app.connections.db import engine
from app.models.base import Base
from app.api import movie_api, producer_api, service_api, studio_api

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(movie_api.router)
app.include_router(producer_api.router)
app.include_router(studio_api.router)
app.include_router(service_api.router)