from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield


app = FastAPI(
    title="Termes Server API",
    lifespan=lifespan
)
