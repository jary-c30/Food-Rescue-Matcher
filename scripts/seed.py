"""Fill the dev database with sample data. Run from the project root: python -m scripts.seed"""

from datetime import datetime, timedelta, timezone

from app.core.database import SessionLocal
from app.models import Donation, DonationStatus, Donor, Driver, Recipient


def main() -> None:
    now = datetime.now(timezone.utc)
    hour = timedelta(hours=1)

    with SessionLocal() as db:
        # Guard so running this twice doesn't duplicate everything.
        if db.query(Donor).first():
            print("Database already has data; skipping.")
            return

        bakery = Donor(name="Sunrise Bakery", address="12 Main St", latitude=40.7128, longitude=-74.0060)
        grocer = Donor(name="Greenway Grocer", address="88 Oak Ave", latitude=40.7306, longitude=-73.9352)
        cafe = Donor(name="Corner Cafe", address="5 Pine Rd", latitude=40.6782, longitude=-73.9442)

        db.add_all(
            [
                bakery,
                grocer,
                cafe,
                Recipient(name="Hope Shelter", address="200 Elm St", latitude=40.7000, longitude=-74.0100, capacity_lbs=300),
                Recipient(name="Community Food Bank", address="9 River Rd", latitude=40.7500, longitude=-73.9800, capacity_lbs=1000),
                Driver(name="Alex Rivera", phone="555-0101", email="alex@example.com"),
                Driver(name="Sam Patel", phone="555-0102", email="sam@example.com", is_available=False),
            ]
        )
        db.flush()  # assigns ids so donations can reference donors

        def donation(donor: Donor, what: str, lbs: float, expires_in: int, status: DonationStatus) -> Donation:
            return Donation(
                donor_id=donor.id,
                description=what,
                quantity_lbs=lbs,
                pickup_start=now,
                pickup_end=now + expires_in * hour,
                expires_at=now + expires_in * hour,
                status=status,
            )

        db.add_all(
            [
                donation(bakery, "Day-old bread", 40, 2, DonationStatus.AVAILABLE),
                donation(bakery, "Pastries", 15, 5, DonationStatus.AVAILABLE),
                donation(grocer, "Produce crates", 120, 24, DonationStatus.AVAILABLE),
                donation(grocer, "Dairy", 60, 1, DonationStatus.MATCHED),
                donation(cafe, "Sandwiches", 25, -3, DonationStatus.EXPIRED),
            ]
        )
        db.commit()
        print("Seeded 3 donors, 2 recipients, 2 drivers, 5 donations.")


if __name__ == "__main__":
    main()
