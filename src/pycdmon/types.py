from __future__ import annotations

from typing import Any, TypedDict


class ApiEnvelope(TypedDict):
    status: str
    data: dict[str, Any] | str


class DomainContact(TypedDict, total=False):
    user_type: int
    name: str
    lastname: str
    identification_type: int
    identification_number: str
    legal_form: int
    province: int
    address: str
    city: str
    country: str
    zipcode: str
    phone: str
    email: str


class DnsNameservers(TypedDict, total=False):
    ns1: str
    ns2: str
    ns3: str
    ns4: str


class DnsRecord(TypedDict, total=False):
    host: str
    type: str
    ttl: int
    destination: str
    priority: int


class ContactModifyPayload(TypedDict, total=False):
    authcode: str
    domain: str
    owner_first_name: str
    owner_surname: str
    owner_esempresa: int
    owner_country: str
    owner_type_nif: int
    owner_nif: str
    owner_state: str
    owner_stateex: str
    owner_city: str
    owner_postal_code: str
    owner_address: str
    owner_phone: str
    owner_email: str


JsonDict = dict[str, Any]
