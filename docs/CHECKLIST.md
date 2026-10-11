# Project Checklist

What is done, in plain language, and what is left. Update this as work lands.

Last updated: 2026-10-11

## Step 1: Scaffolding
- [x] **Git repo and virtual environment.** Version history from day one; `venv/` keeps this project's packages separate from the rest of the machine.
- [x] **Folder structure** (`app/api`, `services`, `models`, `schemas`, `core`, plus `tests/`, `scripts/`). Each layer has one job, so logic stays easy to find and test.
- [x] **Dependencies** in `requirements.txt` (runtime) and `requirements-dev.txt` (tools like pytest and ruff).
- [x] **Config loading** (`app/core/config.py`). Settings come from environment variables, so secrets never live in code. `.env.example` shows the shape; the real `.env` is gitignored.
- [x] **`GET /health` endpoint and test.** The smallest working slice of the app, proving the whole setup runs.
- [x] **README skeleton.** Problem statement, planned features, stack, how to run.

## Step 2: Continuous integration
- [x] **GitHub Actions workflow** (`.github/workflows/ci.yml`). On every push it installs dependencies, runs ruff, then runs pytest on a clean machine.
- [x] **CI badge in the README.** Shows at a glance whether `main` is passing.
- [x] **Pinned ruff version.** CI once failed because a newer ruff than my laptop's added a rule. Pinning keeps lint results the same everywhere.

## Step 3: Database foundation
- [x] **Postgres in Docker** (`docker-compose.yml`). One command starts the database, and `down -v` resets it.
- [x] **SQLAlchemy engine and sessions** (`app/core/database.py`). One session per request through the `get_db` dependency, always closed afterward.
- [x] **Alembic migrations.** Version control for the database structure; reads the URL from app settings so the app and migrations always agree.
- [x] **Explicit driver in the URL** (`postgresql+psycopg2://`). SQLAlchemy 2.x defaults to a different driver that is not installed.

## Step 4: Models and first migration
- [x] **Four models:** `Donor`, `Recipient`, `Driver`, `Donation`. Donors and recipients are separate tables, with shared columns in one mixin.
- [x] **Donation status** stored as text with a CHECK constraint (available, matched, picked_up, delivered, expired). The database rejects invalid values even if app code has a bug.
- [x] **Plain latitude/longitude** columns instead of PostGIS, so distance math stays in testable Python.
- [x] **Initial migration**, tested upgrade, downgrade, upgrade. Alembic autogenerate duplicated a constraint, which I removed by hand.
- [x] **Seed script and practice SQL** (`scripts/seed.py`, `scripts/queries.sql`): sample data plus six queries covering joins, grouping, and a haversine distance calculation.

## Step 5: API layer and test database (in progress)
- [x] **Pydantic schemas** for all four resources. Separate Create and Read shapes, with validation: coordinate ranges, positive quantities, valid emails, timezone-aware times, pickup window in a sensible order.
- [x] **Schema tests** (13 tests, no database needed).
- [x] **`DonationStatus` moved to `app/core/enums.py`** so schemas do not depend on the database layer.
- [x] **Test database created** (`food_rescue_test`), separate from dev data.
- [x] **`TEST_DATABASE_URL` setting**, optional so the app starts without it.
- [x] **`tests/conftest.py` engine fixture.** Safety guards refuse to run unless the target database name ends in `_test` and differs from the dev database. Creates the database if missing and rebuilds the tables once per run.
- [ ] **`db_session` fixture.** Each test runs in a transaction that is rolled back afterward, so tests cannot affect each other.
- [ ] **Isolation test** proving the rollback works.
- [ ] **CRUD endpoints** (create, get one, list) for donors, recipients, drivers, donations; status filter and status update on donations.
- [ ] **API tests** for success and failure cases.
- [ ] **Postgres service in CI**, so database tests run on GitHub, not only locally.

## Later steps
- [ ] **Matching service.** Score donation and recipient pairs (distance, accepted food, capacity, expiry); compare greedy and optimal assignment; unit tests with numbers.
- [ ] **Match and route tables.**
- [ ] **Route grouping** for drivers, with capacity and time-window constraints.
- [ ] **Concurrency safety.** Two matchers must not claim the same donation (row locking), with a test.
- [ ] **Simulation script** producing real metrics for the README.
- [ ] **Map view** (optional) for a README screenshot.
- [ ] **Polish.** Pin all dependency versions, flesh out the README, add a short design doc.
- [ ] **Authentication and deployment** (optional; first things to cut if short on time).
