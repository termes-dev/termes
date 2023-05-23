from contextlib import asynccontextmanager

from fastapi import FastAPI

from termes.server import handlers, services
from termes.services.account.service import AccountService


async def initialize_services(nats_servers: list[str]):
    services.account = AccountService("termes.account")
    await services.account.connect(nats_servers)


async def close_services():
    await services.account.close()


@asynccontextmanager
async def lifespan(application: FastAPI):
    await initialize_services(["nats://0.0.0.0:4222"])
    yield
    await close_services()


def create_application():
    application = FastAPI(
        title="Termes Server API",
        lifespan=lifespan
    )
    application.include_router(handlers.router)
    return application


app = create_application()
