# pycdmon

Professional Python client for cdmon Domains & DNS API.

- Full endpoint coverage for core domain + DNS operations
- Sync and async clients
- Typed payload helpers
- Clean error model (`CdmonApiError`, `CdmonTransportError`)
- Designed for human and agent workflows

## Install

```bash
pip install pycdmon
```

Or from source:

```bash
pip install -e .[dev]
```

## Quickstart

```python
from pycdmon import CdmonDomainsClient

with CdmonDomainsClient(api_key="YOUR_API_KEY") as client:
    result = client.check("example.com")
    print(result["data"]["result"]["available"])
```

## Async usage

```python
import asyncio
from pycdmon import AsyncCdmonDomainsClient

async def main() -> None:
    async with AsyncCdmonDomainsClient(api_key="YOUR_API_KEY") as client:
        print(await client.check("example.com"))

asyncio.run(main())
```

## CLI (`cdmon`)

After installation, a `cdmon` command is available:

```bash
export CDMON_API_KEY="your_api_key"
cdmon check example.com
cdmon info example.com
cdmon balance
cdmon status check
```

You can also pass the key inline:

```bash
cdmon --api-key "$CDMON_API_KEY" check example.com
```

## Supported operations

- Endpoint status: `status`
- Domains: `check`, `info`, `authcode`, `list_domains`, `register`, `renew`, `transfer`, `restore`
- Domain options: `set_block`, `set_whois_private`, `set_dnssec`, `modify_contact`
- DNS: `set_nameservers`, `get_dns_records`, `create_dns_record`, `edit_dns_record`, `delete_dns_record`, `send_dns_key`
- Billing/meta: `get_price`, `get_periods`, `balance`
- Auto-renewal: `get_autorenewal`, `manage_autorenewal`

## Error handling

```python
from pycdmon import CdmonApiError, CdmonDomainsClient

try:
    with CdmonDomainsClient(api_key="...") as client:
        client.transfer("example.com", "wrong-authcode")
except CdmonApiError as exc:
    print(exc.status_code, exc.message)
    print(exc.payload)
```

## Agent-friendly repo workflow

This repository is structured to be easy for coding agents:

- `src/` strict package layout
- `tests/` isolated, deterministic HTTP tests
- `examples/` runnable snippets
- `docs/` implementation and API notes
- CI with lint + tests

Suggested autonomous loop for agents:

1. Add/update behavior in `src/pycdmon`
2. Add/adjust tests in `tests/`
3. Run `ruff check . && pytest`
4. Keep commits small and descriptive

## API reference source

Based on cdmon official API docs:
https://apidedominioscat.docs.apiary.io/#introduction/endpoints-disponibles

## License

MIT
