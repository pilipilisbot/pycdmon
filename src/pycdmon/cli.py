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

    status = sub.add_parser("status", help="Check if endpoint action is available")
    status.add_argument("action", help="action name, e.g. check, renew, getprice")

    domains = sub.add_parser("domains", help="List domains")
    domains.add_argument("--no-extended-info", action="store_true", help="Disable extended info")

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
            elif args.command == "status":
                _print_json(client.status(args.action))
            elif args.command == "domains":
                _print_json(client.list_domains(extended_info=not args.no_extended_info))
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
