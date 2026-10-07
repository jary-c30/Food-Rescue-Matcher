# Importing every model here registers it on Base.metadata so Alembic can see it.
from app.models.donation import Donation, DonationStatus
from app.models.donor import Donor
from app.models.driver import Driver
from app.models.recipient import Recipient

__all__ = ["Donation", "DonationStatus", "Donor", "Driver", "Recipient"]
