# Food Rescue Matcher

[![CI](https://github.com/jary-c30/Food-Rescue-Matcher/actions/workflows/ci.yml/badge.svg)](https://github.com/jary-c30/Food-Rescue-Matcher/actions/workflows/ci.yml)

Every day, restaurants and grocers throw away edible food while shelters and food banks nearby go short. Closing that gap is hard because pickups are time-sensitive, donations are irregular, and volunteer drivers have limited time. Food Rescue Matcher matches surplus food from donors to the recipients that need it, then groups pickups into efficient routes for volunteer drivers.

## Planned Features

- Donor listings of surplus food (quantity, category, pickup window, expiry)
- Recipient profiles with needs, capacity, and accepted food types
- Matching of donations to recipients
- Grouping of pickups into routes for volunteer drivers
- Driver assignment and pickup status tracking
- Authentication and role-based access (donor, recipient, driver, admin)

## Planned Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL, SQLAlchemy
- **Config:** pydantic-settings
- **Testing and linting:** pytest, httpx, ruff
- **CI:** GitHub Actions

## How to Run Locally

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements-dev.txt

# 3. Configure environment variables
cp .env.example .env   # then edit the values

# 4. Start the API
uvicorn app.main:app --reload

# 5. Check it is running
curl http://localhost:8000/health

# 6. Run the tests
pytest
```
