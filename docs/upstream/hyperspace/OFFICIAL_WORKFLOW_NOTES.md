# Hyperspace Official Workflow Notes (Docs-Derived)

Source files:
- `quick-start.md`
- `installing-api-client.md`
- `schema-config.md`

## 1) Access model from official docs

The docs describe API access through client credentials and host address:
- install client (`pip install hyperspace-py`)
- create client with `host`, `username`, `password`

Evidence:
- `quick-start.md` lines 16, 37-47
- `installing-api-client.md` lines 5, 16

## 2) Documented onboarding flow

Official sequence in quick start:
1. Install client
2. Instantiate local client with credentials
3. Create schema
4. Create collection
5. Upload batch data and commit
6. Build and run queries

Evidence:
- `quick-start.md` lines 5-7, 35-37, 77-92, 203-222, 286+

## 3) Schema expectations

Schema is required and can be provided as JSON or dictionary under `configuration`.
Supports metadata fields and `dense_vector` fields plus index options.

Evidence:
- `schema-config.md` lines 3-10, 15-33, 88

## 4) Benchmarking implications for this repo

To avoid assumptions and align with upstream docs:
- Prefer testing authenticated API paths where possible.
- Support `host + username + password` auth path in benchmark harness.
- Keep any bearer/API-key path optional unless official docs specify it.

## 5) Required input before final collab-grade benchmark run

- Official target endpoint(s) to benchmark
- Authentication type in use in your deployment
  - username/password (docs-default)
  - or token/key if your environment is configured that way
- Any endpoint-specific request body schema for POST workloads
