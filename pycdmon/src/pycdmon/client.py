from __future__ import annotations

from typing import Any

import httpx

from .errors import CdmonApiError, CdmonTransportError
from .types import ContactModifyPayload, DnsNameservers, DnsRecord, JsonDict

DEFAULT_BASE_URL = "https://api-domains.cdmon.services/api-domains/"


class CdmonDomainsClient:
    """Synchronous client for cdmon Domains & DNS API."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 20.0,
        client: httpx.Client | None = None,
    ) -> None:
        if not api_key.strip():
            raise ValueError("api_key cannot be empty")

        self._owns_client = client is None
        self._client = client or httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={
                "Accept": "application/json",
                "apikey": api_key,
                "Content-Type": "application/json",
            },
        )

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "CdmonDomainsClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _post(self, endpoint: str, data: JsonDict | None = None) -> JsonDict:
        payload: JsonDict = {} if data is None else {"data": data}
        try:
            response = self._client.post(endpoint, json=payload)
        except httpx.HTTPError as exc:
            raise CdmonTransportError(f"Transport error calling {endpoint}: {exc}") from exc

        body: JsonDict
        try:
            body = response.json()
        except ValueError as exc:
            raise CdmonApiError(
                message="Invalid JSON response from cdmon",
                status_code=response.status_code,
                payload=None,
            ) from exc

        if response.status_code >= 400:
            raise CdmonApiError(
                message=_extract_error_message(body),
                status_code=response.status_code,
                payload=body,
            )

        if body.get("status") == "ko":
            raise CdmonApiError(
                message=_extract_error_message(body),
                status_code=response.status_code,
                payload=body,
            )

        return body

    # Generic
    def status(self, action: str) -> JsonDict:
        return self._post("status", {"action": action})

    # Domains
    def check(self, domain: str) -> JsonDict:
        return self._post("check", {"domain": domain})

    def info(self, domain: str, authcode: str | None = None) -> JsonDict:
        data: JsonDict = {"domain": domain}
        if authcode:
            data["authcode"] = authcode
        return self._post("info", data)

    def authcode(self, domain: str) -> JsonDict:
        return self._post("authcode", {"domain": domain, "action": "get"})

    def list_domains(self, *, extended_info: bool = True) -> JsonDict:
        return self._post("domains/list", {"extended_info": 1 if extended_info else 0})

    def register(self, domain: str, period: int, intended_use: str, contact: JsonDict) -> JsonDict:
        return self._post(
            "register",
            {
                "domain": domain,
                "period": period,
                "intended_use": intended_use,
                "contact": contact,
            },
        )

    def renew(self, domain: str, period: int) -> JsonDict:
        return self._post("renew", {"domain": domain, "period": str(period)})

    def transfer(self, domain: str, authcode: str) -> JsonDict:
        return self._post("transfer", {"domain": domain, "authcode": authcode})

    def restore(self, domain: str) -> JsonDict:
        return self._post("restore", {"domain": domain, "action": "restore"})

    # Contact / privacy / domain options
    def set_block(self, domain: str, enabled: bool) -> JsonDict:
        return self._post("block", {"domain": domain, "action": "block" if enabled else "unblock"})

    def set_whois_private(self, domain: str, enabled: bool) -> JsonDict:
        return self._post(
            "whoisprivate", {"domain": domain, "action": "enable" if enabled else "disable"}
        )

    def set_dnssec(self, domain: str, enabled: bool) -> JsonDict:
        return self._post("dnssec", {"domain": domain, "action": "enable" if enabled else "disable"})

    def modify_contact(self, payload: ContactModifyPayload) -> JsonDict:
        return self._post("contacts/modify", dict(payload))

    # DNS
    def set_nameservers(self, domain: str, nameservers: DnsNameservers) -> JsonDict:
        return self._post("dns", {"domain": domain, "ns": dict(nameservers)})

    def get_dns_records(self, domain: str) -> JsonDict:
        return self._post("getDnsRecords", {"domain": domain})

    def create_dns_record(self, domain: str, record: DnsRecord) -> JsonDict:
        return self._post("dnsrecords/create", {"domain": domain, **dict(record)})

    def edit_dns_record(self, domain: str, current: JsonDict, new: JsonDict) -> JsonDict:
        return self._post("dnsrecords/edit", {"domain": domain, "current": current, "new": new})

    def delete_dns_record(self, domain: str, *, host: str, type_: str) -> JsonDict:
        return self._post("dnsrecords/delete", {"domain": domain, "host": host, "type": type_})

    def send_dns_key(
        self,
        domain: str,
        *,
        key_type: str,
        algorithm: int,
        flags: int,
        pubkey: str,
        digest_type: int | None = None,
        digest: str | None = None,
    ) -> JsonDict:
        data: JsonDict = {
            "domain": domain,
            "type": key_type,
            "algorithm": algorithm,
            "flags": flags,
            "pubKey": pubkey,
        }
        if digest_type is not None:
            data["digestType"] = digest_type
        if digest is not None:
            data["digest"] = digest
        return self._post("sendDnsKey", data)

    # Billing
    def get_price(self, tld: str, action: str) -> JsonDict:
        return self._post("getPrice", {"tld": tld, "action": action})

    def get_periods(self, tld: str, action: str) -> JsonDict:
        return self._post("getPeriods", {"tld": tld, "action": action})

    def balance(self) -> JsonDict:
        return self._post("balance")

    # Auto renewal
    def get_autorenewal(self, domain: str) -> JsonDict:
        return self._post("autorenewal", {"domain": domain})

    def manage_autorenewal(
        self,
        domain: str,
        *,
        enabled: bool,
        payment_method: str = "card",
    ) -> JsonDict:
        return self._post(
            "autorenewal/manage",
            {
                "domain": domain,
                "action": "enable" if enabled else "disable",
                "payment_method": payment_method,
            },
        )


class AsyncCdmonDomainsClient:
    """Asynchronous client for cdmon Domains & DNS API."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 20.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not api_key.strip():
            raise ValueError("api_key cannot be empty")
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={
                "Accept": "application/json",
                "apikey": api_key,
                "Content-Type": "application/json",
            },
        )

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> "AsyncCdmonDomainsClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    async def _post(self, endpoint: str, data: JsonDict | None = None) -> JsonDict:
        payload: JsonDict = {} if data is None else {"data": data}
        try:
            response = await self._client.post(endpoint, json=payload)
        except httpx.HTTPError as exc:
            raise CdmonTransportError(f"Transport error calling {endpoint}: {exc}") from exc

        try:
            body: JsonDict = response.json()
        except ValueError as exc:
            raise CdmonApiError(
                message="Invalid JSON response from cdmon",
                status_code=response.status_code,
                payload=None,
            ) from exc

        if response.status_code >= 400 or body.get("status") == "ko":
            raise CdmonApiError(_extract_error_message(body), response.status_code, body)

        return body

    async def check(self, domain: str) -> JsonDict:
        return await self._post("check", {"domain": domain})


def _extract_error_message(body: JsonDict) -> str:
    data = body.get("data")
    if isinstance(data, dict):
        if "msg" in data and isinstance(data["msg"], str):
            return data["msg"]
        if "errors" in data and isinstance(data["errors"], list):
            return "; ".join(str(x) for x in data["errors"])
    if isinstance(data, str):
        return data
    return "Unknown cdmon API error"
