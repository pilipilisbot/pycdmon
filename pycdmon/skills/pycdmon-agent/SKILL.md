---
name: pycdmon-agent
description: Operate cdmon Domains & DNS service using the pycdmon SDK and CLI. Use when an agent must execute real domain or DNS operations (availability checks, info, transfer/renew workflows, DNS record management, pricing/periods, balance, endpoint status), prepare safe command snippets, or troubleshoot cdmon API usage.
---

# pycdmon Agent Skill

Use this skill to **run cdmon operations safely and correctly**, not to develop the library.

## 1) Configure authentication safely

- Prefer environment variable:

```bash
export CDMON_API_KEY="<your_api_key>"
```

- Or pass inline only when needed:

```bash
cdmon --api-key "$CDMON_API_KEY" check example.com
```

- Never expose API keys in logs, docs, screenshots, or commits.

## 2) Verify service/API status first

Run a health check before critical operations:

```bash
cdmon status check
```

If status fails, stop destructive or billing-impact actions and report clearly.

## 3) Common operational commands

### Domain checks and info

```bash
cdmon check example.com
cdmon info example.com
cdmon authcode example.com
```

### Lifecycle actions

```bash
cdmon renew example.com --period 1
cdmon transfer example.com 'AUTH-CODE'
```

### DNS management

```bash
cdmon dns-records example.com
cdmon dns-create example.com --host @ --type A --destination 1.2.3.4 --ttl 900
cdmon dns-delete example.com --host @ --type A
```

### Pricing and account

```bash
cdmon price com create
cdmon periods com renew
cdmon balance
```

## 4) Apply safe-change workflow for DNS/domain updates

- Inspect current state first (`info`, `dns-records`).
- Propose exact changes and expected outcome.
- Execute minimal change set.
- Re-read state to verify.
- Report both command + resulting state.

## 5) Prefer explicit, auditable operations

- Use narrow commands with concrete arguments.
- Avoid broad or ambiguous bulk edits unless explicitly requested.
- For risky operations (transfer/renew/delete), confirm target domain and parameters.

## 6) Troubleshooting guidance

- If API errors occur, capture status/message and map to action:
  - auth/permission issues → verify API key and account scope
  - validation issues → fix domain/TLD/record parameters
  - transport issues → retry after checking connectivity/status endpoint
- Keep retries bounded; avoid loops.

## 7) Keep agent guidance aligned with repo capabilities

When pycdmon CLI or supported operations change, update this skill so it always matches:

- `README.md`
- available `cdmon` commands
- service workflows currently supported by the SDK/CLI
