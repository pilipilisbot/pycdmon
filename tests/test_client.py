from __future__ import annotations

import httpx
import pytest

from pycdmon import CdmonApiError, CdmonDomainsClient


@pytest.fixture
def transport_ok() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/check"):
            payload = request.read().decode()
            assert '"domain":"example.com"' in payload
            return httpx.Response(
                200,
                json={"status": "ok", "data": {"result": {"available": True}}},
            )
        return httpx.Response(200, json={"status": "ok", "data": {"msg": "ok"}})

    return httpx.MockTransport(handler)


def test_check_domain_success(transport_ok: httpx.MockTransport) -> None:
    client = httpx.Client(
        base_url="https://api-domains.cdmon.services/api-domains/",
        headers={"apikey": "x", "Accept": "application/json", "Content-Type": "application/json"},
        transport=transport_ok,
    )

    sdk = CdmonDomainsClient(api_key="x", client=client)
    response = sdk.check("example.com")
    assert response["status"] == "ok"
    assert response["data"]["result"]["available"] is True


def test_ko_status_raises_api_error() -> None:
    transport = httpx.MockTransport(
        lambda _req: httpx.Response(200, json={"status": "ko", "data": {"msg": "bad auth"}})
    )
    client = httpx.Client(
        base_url="https://api-domains.cdmon.services/api-domains/",
        headers={"apikey": "x", "Accept": "application/json", "Content-Type": "application/json"},
        transport=transport,
    )

    sdk = CdmonDomainsClient(api_key="x", client=client)
    with pytest.raises(CdmonApiError) as exc:
        sdk.balance()

    assert exc.value.status_code == 200
    assert "bad auth" in str(exc.value)


def test_http_error_raises_api_error() -> None:
    transport = httpx.MockTransport(
        lambda _req: httpx.Response(403, json={"status": "ko", "data": "forbidden"})
    )
    client = httpx.Client(
        base_url="https://api-domains.cdmon.services/api-domains/",
        headers={"apikey": "x", "Accept": "application/json", "Content-Type": "application/json"},
        transport=transport,
    )

    sdk = CdmonDomainsClient(api_key="x", client=client)
    with pytest.raises(CdmonApiError) as exc:
        sdk.check("example.com")

    assert exc.value.status_code == 403
    assert "forbidden" in exc.value.message
