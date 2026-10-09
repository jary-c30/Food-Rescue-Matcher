# Project Notes

Working notes so the project can be picked up without the original chat history.

## Goal
Resume project for Summer 2027 internship applications: a FastAPI + PostgreSQL app that matches surplus food from donors (restaurants, grocers) to recipients (shelters, food banks) and groups pickups into routes for volunteer drivers.

## Status (as of 2026-10-08)
- [x] Step 1: scaffolding (folders, config, `/health` endpoint + test, README)
- [x] Step 2: GitHub Actions CI (ruff + pytest)
- [x] Step 3: database foundation (SQLAlchemy, Alembic, Postgres via Docker Compose)
- [x] Step 4: models (`Donor`, `Recipient`, `Driver`, `Donation`) + initial migration
- [x] Extras: `scripts/seed.py`, `scripts/queries.sql`
- [ ] Step 5: Pydantic schemas + CRUD endpoints, test database, Postgres service in CI
- [ ] Matching service (with unit tests and a baseline comparison)
- [ ] Match/route tables and route grouping (driver capacity, time windows)
- [ ] Simulation script producing metrics for the README
- [ ] Optional: map frontend (Leaflet), row-locking concurrency test, design doc
- [ ] Polish: pin dependency versions, README details/screenshots

## Architecture: why the folders are separate
- `app/api/`: HTTP layer only (routes, status codes). No business rules.
- `app/services/`: business logic (matching, routing). No HTTP knowledge, so it is unit-testable.
- `app/models/`: SQLAlchemy classes describing database tables.
- `app/schemas/`: Pydantic classes describing what the API accepts/returns (kept separate from models so DB changes don't break the API and fields don't leak).
- `app/core/`: config, database engine/session, shared infrastructure.

Request flow: `api` validates with a schema -> calls a `service` -> reads/writes `models`.

## Design decisions
- **Separate `donors` and `recipients` tables** (not one `organizations` table): each has only the columns it needs; foreign keys stay clear. Shared columns live in `OrganizationMixin`.
- **Plain latitude/longitude floats, not PostGIS**: distance math (haversine) stays in testable Python. PostGIS is a possible later upgrade.
- **`donations.status` as string + CHECK constraint, not a native Postgres enum**: adding a status later is a simple constraint change. Values: available, matched, picked_up, delivered, expired.
- **Database URL uses `postgresql+psycopg2://`**: SQLAlchemy 2.x defaults plain `postgresql://` to psycopg v3, which is not installed.
- **Alembic reads `DATABASE_URL` from app settings** (`migrations/env.py`), so the app and migrations always agree.

## Running locally
```bash
source venv/bin/activate
cp .env.example .env            # values already match docker-compose.yml
docker compose up -d            # Postgres 17
alembic upgrade head            # create tables
python -m scripts.seed          # optional sample data
uvicorn app.main:app --reload
pytest
```
Practice SQL: `docker compose exec -T db psql -U food_rescue < scripts/queries.sql`

Reset the database: `docker compose down -v`, then `docker compose up -d` and `alembic upgrade head`.

If `docker` is not found in a terminal, open a new terminal, or run
`export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"`.

## Gotchas hit so far
- Homebrew Postgres failed (Command Line Tools too old), so Docker Desktop is used instead.
- Alembic autogenerate duplicated the status CHECK constraint; the duplicate was removed by hand in the migration.
- `app.core.config` builds `Settings()` on import, so CI sets dummy `DATABASE_URL`, `SECRET_KEY`, `ENVIRONMENT`.
- Starlette's `TestClient` shows a deprecation warning about `httpx` (harmless).

## Ideas that would make the project stand out
1. Matching as a scored, defensible algorithm (distance, accepted food types, capacity, expiry); compare greedy vs optimal assignment (Hungarian) with numbers.
2. Simulation script with hundreds of random records, reporting pounds rescued, miles driven, expired donations.
3. Routing with real constraints (capacity, time windows); nearest-neighbor + 2-opt vs naive.
4. Serious tests: unit tests for services, API tests on a real test DB, Postgres in CI.
5. Map view (Leaflet) with a README screenshot; `SELECT ... FOR UPDATE` concurrency test; one-page design doc.
Skip: microservices, Kubernetes, queues, ML. Be honest in the README: no real users, simple routing is a heuristic.

## Estimate
About 2 more weeks at 2-3 hours/day for a resume-ready version (no auth, no deployment); 3 weeks at a relaxed pace.
