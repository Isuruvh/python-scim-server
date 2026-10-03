# Python SCIM Server

A small, local **SCIM 2.0** server built with Python and Flask. It simulates an HRIS "worker" directory so an Identity Provider (IdP, e.g. Okta) can provision and import users. The IdP reaches your machine through an **ngrok** tunnel and authenticates with a **Bearer token** in the `Authorization` header.

> For development and testing only. Data is held in memory and lost on restart, and the token is hardcoded.

## Project structure

| File | Purpose |
|------|---------|
| `app.py` | Flask SCIM server (port 8000) with Bearer token check |
| `seed_db.py` | Posts users from `scim_sample_users.json` to the running server |
| `scim_sample_users.json` | Sample SCIM users used for seeding |
| `hr_import_workers.csv` | Sample HR worker data (CSV) for reference/imports |
| `workers_db.py` | Standalone sample worker dataset (not imported by `app.py`) |

## Prerequisites

- Python 3.9+
- [ngrok](https://ngrok.com/download) with an authtoken configured (`ngrok config add-authtoken <TOKEN>`)
- An IdP tenant (e.g. Okta) with a SCIM 2.0 app integration

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install flask
```

On macOS/Linux: `source .venv/bin/activate`.

## Run

1. Start the server (listens on `http://localhost:8000`):

   ```powershell
   python app.py
   ```

2. In a second terminal, start ngrok:

   ```powershell
   ngrok http 8000
   ```

   Copy the HTTPS forwarding URL, e.g. `https://abcd-1234.ngrok-free.app`.

3. (Optional) Seed sample users:

   ```powershell
   python seed_db.py
   ```

## Authentication

The server expects header-based authentication on every request:

```
Authorization: Bearer test-token-12345
```

The token is defined as `BEARER_TOKEN` in [app.py](app.py). Change it before sharing the tunnel URL, and use the same value in the IdP.

## IdP configuration (Okta example)

In your SCIM app's **Provisioning → Integration** settings:

| Field | Value |
|-------|-------|
| SCIM connector base URL | `https://<your-ngrok-host>/scim/v2` |
| Unique identifier field for users | `userName` |
| Authentication Mode | **HTTP Header** |
| Authorization (Bearer token) | `test-token-12345` (or your own token) |

Supported actions: Import New Users and Profile Updates, Push New Users, Push Profile Updates. Use **Test Connector Configuration** to verify.

## Endpoints

Base path: `/scim/v2`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/Users` | List users (SCIM ListResponse) |
| GET | `/Users/<id>` | Get a user by id |
| POST | `/Users` | Create a user (id generated as `hr-worker-<timestamp>`) |
| PUT | `/Users/<id>` | Replace a user |
| PATCH | `/Users/<id>` | Update `active` via `replace` operations |
| GET | `/Groups` | Returns an empty list |

Missing/invalid token returns `401`.

## Quick test

```powershell
curl -H "Authorization: Bearer test-token-12345" http://localhost:8000/scim/v2/Users
curl -H "Authorization: Bearer test-token-12345" https://<your-ngrok-host>/scim/v2/Users
```

The Flask console prints each inbound IdP request, which is useful for debugging.

## Notes

- ngrok free URLs change on each restart; update the IdP base URL when that happens.
- `debug=True` and `host=0.0.0.0` are set in `app.py`; do not expose this beyond local testing.
