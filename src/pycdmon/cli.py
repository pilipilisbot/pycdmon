from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from .client import CdmonDomainsClient
from .errors import CdmonApiError, CdmonTransportError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cdmon", description="CLI for cdmon Domains & DNS API")
    parser.add_argument("--api-key", default=None, help="cdmon API key (or use CDMON_API_KEY)")
    parser.add_argument(
        "--base-url",
        default="https://api-domains.cdmon.services/api-domains/",
        help="API base URL",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="Check domain availability")
    check.add_argument("domain")

    info = sub.add_parser("info", help="Get domain information")
    info.add_argument("domain")
    info.add_argument("--authcode", default=None)

    authcode = sub.add_parser("authcode", help="Get domain authcode")
    authcode.add_argument("domain")

    status = sub.add_parser("status", help="Check if endpoint action is available")
    status.add_argument("action", help="action name, e.g. check, renew, getprice")

    domains = sub.add_parser("domains", help="List domains")
    domains.add_argument("--no-extended-info", action="store_true", help="Disable extended info")

    renew = sub.add_parser("renew", help="Renew domain")
    renew.add_argument("domain")
    renew.add_argument("--period", type=int, default=1)

    transfer = sub.add_parser("transfer", help="Transfer domain")
    transfer.add_argument("domain")
    transfer.add_argument("authcode")

    restore = sub.add_parser("restore", help="Restore domain")
    restore.add_argument("domain")

    autore = sub.add_parser("autorenewal", help="Get domain auto-renewal status")
    autore.add_argument("domain")

    autore_manage = sub.add_parser("autorenewal-manage", help="Enable/disable domain auto-renewal")
    autore_manage.add_argument("domain")
    autore_manage.add_argument("action", choices=["enable", "disable"])
    autore_manage.add_argument("--payment-method", default="card")

    dns = sub.add_parser("dns-records", help="List DNS records")
    dns.add_argument("domain")

    dns_create = sub.add_parser("dns-create", help="Create DNS record")
    dns_create.add_argument("domain")
    dns_create.add_argument("--host", required=True)
    dns_create.add_argument("--type", dest="type_", required=True)
    dns_create.add_argument("--destination", required=True)
    dns_create.add_argument("--ttl", type=int, default=900)
    dns_create.add_argument("--priority", type=int)

    dns_delete = sub.add_parser("dns-delete", help="Delete DNS record")
    dns_delete.add_argument("domain")
    dns_delete.add_argument("--host", required=True)
    dns_delete.add_argument("--type", dest="type_", required=True)

    get_price = sub.add_parser("price", help="Get operation price by TLD")
    get_price.add_argument("tld")
    get_price.add_argument("action", choices=["create", "renew", "transfer", "restore"])

    get_periods = sub.add_parser("periods", help="Get allowed periods by TLD")
    get_periods.add_argument("tld")
    get_periods.add_argument("action", choices=["create", "renew"])

    sub.add_parser("balance", help="Get account balance summary")

    return parser


def _print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    api_key = args.api_key or os.getenv("CDMON_API_KEY")
    if not api_key:
        parser.error("Missing API key. Use --api-key or set CDMON_API_KEY")

    try:
        with CdmonDomainsClient(api_key=api_key, base_url=args.base_url) as client:
            if args.command == "check":
                _print_json(client.check(args.domain))
            elif args.command == "info":
                _print_json(client.info(args.domain, authcode=args.authcode))
            elif args.command == "authcode":
                _print_json(client.authcode(args.domain))
            elif args.command == "status":
                _print_json(client.status(args.action))
            elif args.command == "domains":
                _print_json(client.list_domains(extended_info=not args.no_extended_info))
            elif args.command == "renew":
                _print_json(client.renew(args.domain, period=args.period))
            elif args.command == "transfer":
                _print_json(client.transfer(args.domain, authcode=args.authcode))
            elif args.command == "restore":
                _print_json(client.restore(args.domain))
            elif args.command == "autorenewal":
                _print_json(client.get_autorenewal(args.domain))
            elif args.command == "autorenewal-manage":
                _print_json(
                    client.manage_autorenewal(
                        args.domain,
                        enabled=args.action == "enable",
                        payment_method=args.payment_method,
                    )
                )
            elif args.command == "dns-records":
                _print_json(client.get_dns_records(args.domain))
            elif args.command == "dns-create":
                record: dict[str, Any] = {
                    "host": args.host,
                    "type": args.type_,
                    "ttl": args.ttl,
                    "destination": args.destination,
                }
                if args.priority is not None:
                    record["priority"] = args.priority
                _print_json(client.create_dns_record(args.domain, record=record))
            elif args.command == "dns-delete":
                _print_json(client.delete_dns_record(args.domain, host=args.host, type_=args.type_))
            elif args.command == "price":
                _print_json(client.get_price(args.tld, args.action))
            elif args.command == "periods":
                _print_json(client.get_periods(args.tld, args.action))
            elif args.command == "balance":
                _print_json(client.balance())
            else:
                parser.error(f"Unknown command: {args.command}")
    except CdmonApiError as exc:
        print(str(exc), file=sys.stderr)
        if exc.payload is not None:
            print(json.dumps(exc.payload, indent=2, ensure_ascii=False), file=sys.stderr)
        return 2
    except CdmonTransportError as exc:
        print(str(exc), file=sys.stderr)
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
