from __future__ import annotations

import asyncio

import httpx
import pytest

from pycdmon import AsyncCdmonDomainsClient, CdmonApiError, CdmonTransportError


def test_async_balance_success() -> None:
    async def run() -> None:
        transport = httpx.MockTransport(
            lambda _req: httpx.Response(200, json={"status": "ok", "data": {"amount": "12.34"}})
        )
        client = httpx.AsyncClient(
            base_url="https://api-domains.cdmon.services/api-domains/",
            headers={
                "apikey": "x",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            transport=transport,
        )

        sdk = AsyncCdmonDomainsClient(api_key="x", client=client)
        response = await sdk.balance()
        assert response["status"] == "ok"
        assert response["data"]["amount"] == "12.34"

    asyncio.run(run())


def test_async_ko_status_raises_api_error() -> None:
    async def run() -> None:
        transport = httpx.MockTransport(
            lambda _req: httpx.Response(200, json={"status": "ko", "data": {"msg": "bad auth"}})
        )
        client = httpx.AsyncClient(
            base_url="https://api-domains.cdmon.services/api-domains/",
            headers={
                "apikey": "x",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            transport=transport,
        )

        sdk = AsyncCdmonDomainsClient(api_key="x", client=client)
        with pytest.raises(CdmonApiError) as exc:
            await sdk.get_autorenewal("example.com")

        assert exc.value.status_code == 200
        assert "bad auth" in str(exc.value)

    asyncio.run(run())


def test_async_invalid_json_raises_api_error() -> None:
    async def run() -> None:
        transport = httpx.MockTransport(lambda _req: httpx.Response(200, text="not-json"))
        client = httpx.AsyncClient(
            base_url="https://api-domains.cdmon.services/api-domains/",
            headers={
                "apikey": "x",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            transport=transport,
        )

        sdk = AsyncCdmonDomainsClient(api_key="x", client=client)
        with pytest.raises(CdmonApiError) as exc:
            await sdk.balance()

        assert exc.value.status_code == 200
        assert "Invalid JSON response" in exc.value.message

    asyncio.run(run())


def test_async_transport_error_raises_transport_error() -> None:
    async def run() -> None:
        def handler(_req: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("boom")

        transport = httpx.MockTransport(handler)
        client = httpx.AsyncClient(
            base_url="https://api-domains.cdmon.services/api-domains/",
            headers={
                "apikey": "x",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            transport=transport,
        )

        sdk = AsyncCdmonDomainsClient(api_key="x", client=client)
        with pytest.raises(CdmonTransportError) as exc:
            await sdk.check("example.com")

        assert "Transport error calling check" in str(exc.value)

    asyncio.run(run())
