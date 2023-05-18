from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from termes import database
from termes.application import handlers, settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    database.engine = create_async_engine(settings.DATABASE_URL)
    database.sessionmaker = async_sessionmaker(database.engine, expire_on_commit=False)
    application.include_router(handlers.router)
    yield


app = FastAPI(lifespan=lifespan)
