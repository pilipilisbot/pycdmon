from __future__ import annotations

import json

from pycdmon import cli


class FakeClient:
    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url

    def __enter__(self) -> FakeClient:
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def check(self, domain: str) -> dict[str, object]:
        return {"status": "ok", "data": {"domain": domain}}

    def renew(self, domain: str, period: int) -> dict[str, object]:
        return {"status": "ok", "data": {"domain": domain, "period": period}}

    def create_dns_record(self, domain: str, record: dict[str, object]) -> dict[str, object]:
        return {"status": "ok", "data": {"domain": domain, "record": record}}


def test_cli_check(monkeypatch, capsys) -> None:
    monkeypatch.setenv("CDMON_API_KEY", "k")
    monkeypatch.setattr(cli, "CdmonDomainsClient", FakeClient)

    code = cli.main(["check", "example.com"])

    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["data"]["domain"] == "example.com"


def test_cli_renew(monkeypatch, capsys) -> None:
    monkeypatch.setenv("CDMON_API_KEY", "k")
    monkeypatch.setattr(cli, "CdmonDomainsClient", FakeClient)

    code = cli.main(["renew", "example.com", "--period", "2"])

    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["data"]["period"] == 2


def test_cli_dns_create(monkeypatch, capsys) -> None:
    monkeypatch.setenv("CDMON_API_KEY", "k")
    monkeypatch.setattr(cli, "CdmonDomainsClient", FakeClient)

    code = cli.main(
        [
            "dns-create",
            "example.com",
            "--host",
            "@",
            "--type",
            "A",
            "--destination",
            "1.2.3.4",
            "--ttl",
            "600",
        ]
    )

    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["data"]["record"]["host"] == "@"
    assert payload["data"]["record"]["ttl"] == 600
