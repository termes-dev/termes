from contextlib import asynccontextmanager

from fastapi import FastAPI

from termes import handlers


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.include_router(handlers.router)
    yield


app = FastAPI(
    title="Termes Server API",
    lifespan=lifespan
)
