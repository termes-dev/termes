import msgpack
import nats
from nats.aio.client import Client
from typing_extensions import Self

from ..services.types import ServiceRequest, ServiceResponse


class Service:
    def __init__(self, name: str):
        self.name = name
        self.nats_client: Client | None = None

    async def connect(self, nats_servers: list[str]):
        self.nats_client = await nats.connect(nats_servers)

    async def request(
            self,
            endpoint: str,
            request: ServiceRequest,
            response_model: type[ServiceResponse],
            *,
            timeout: float = 0.5
    ) -> ServiceResponse:
        response = await self.nats_client.request(
            subject=f"{self.name}.{endpoint}",
            payload=msgpack.packb(request.dict()),
            timeout=timeout
        )
        return response_model.parse_obj(msgpack.unpackb(response.data))

    async def close(self):
        await self.nats_client.drain()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
