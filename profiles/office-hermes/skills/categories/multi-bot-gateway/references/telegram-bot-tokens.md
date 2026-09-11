# Telegram Bot Tokens — Multi-Bot Gateway Setup

Session: 2026-09-10. Mahesh's Hermes AI Employees (RBAC) at `~/.hermes/ops/`.

## Token env var → bot username mapping

| Role      | Env var                         | Bot username         | Token OK |
|-----------|----------------------------------|----------------------|----------|
| CEO       | `TELEGRAM_BOT_TOKEN`            | (default Hermes)    | live     |
| CMO       | `HERMES_CMO_TELEGRAM_TOKEN`     | @Dci_cmohermesbot   | verified |
| Manager   | `HERMES_MANAGER_TELEGRAM_TOKEN` | @Dci_managerbot     | verified |
| Employee  | `HERMES_EMPLOYEE_TELEGRAM_TOKEN`| @Dci_employeebot    | verified |
| CTO       | `HERMES_CTO_TELEGRAM_TOKEN`     | (pending)           | not set  |

## Verification method

Hit `https://api.telegram.org/bot<TOKEN>/getMe` and check `ok: true` + `result.username`.

Python one-liner:
```python
import os, json, urllib.request
tok = os.environ["HERMES_CMO_TELEGRAM_TOKEN"]
url = f"https://api.telegram.org/bot{tok}/getMe"
req = urllib.request.Request(url)
with urllib.request.urlopen(req, timeout=10) as r:
    d = json.loads(r.read())
    print("OK" if d["ok"] else "FAIL", d.get("result", {}).get("username"))
```

## Notes

- CEO bot is the default Hermes gateway; it runs as pid 1187 (from `gateway_state.json`).
- All three role bot gateways were launched on 2026-09-10 and confirmed connected.
- CTO token (`HERMES_CTO_TELEGRAM_TOKEN`) was NOT set in the environment at time of writing — launching a CTO gateway will fail until it is.
