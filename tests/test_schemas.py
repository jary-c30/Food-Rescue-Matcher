from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.core.enums import DonationStatus
from app.schemas import (
    DonationCreate,
    DonationRead,
    DonorCreate,
    DonorRead,
    DriverCreate,
    RecipientCreate,
)

NOW = datetime(2026, 10, 9, 12, 0, tzinfo=UTC)
HOUR = timedelta(hours=1)


def donor_data(**overrides: object) -> dict[str, object]:
    return {"name": "Sunrise Bakery", "address": "12 Main St", "latitude": 40.7, "longitude": -74.0} | overrides


def donation_data(**overrides: object) -> dict[str, object]:
    return {
        "donor_id": 1,
        "description": "Day-old bread",
        "quantity_lbs": 40,
        "pickup_start": NOW,
        "pickup_end": NOW + 2 * HOUR,
        "expires_at": NOW + 3 * HOUR,
    } | overrides


def test_valid_donor_is_accepted() -> None:
    donor = DonorCreate(**donor_data())

    assert donor.phone is None


@pytest.mark.parametrize("field, value", [("latitude", 91), ("latitude", -91), ("longitude", 181), ("name", "")])
def test_donor_rejects_bad_values(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        DonorCreate(**donor_data(**{field: value}))


@pytest.mark.parametrize("capacity", [0, -5])
def test_recipient_capacity_must_be_positive(capacity: float) -> None:
    with pytest.raises(ValidationError):
        RecipientCreate(**donor_data(capacity_lbs=capacity))


def test_driver_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        DriverCreate(name="Alex", email="not-an-email")


def test_valid_donation_is_accepted() -> None:
    assert DonationCreate(**donation_data()).quantity_lbs == 40


@pytest.mark.parametrize(
    "overrides",
    [
        {"quantity_lbs": 0},
        {"pickup_end": NOW},  # ends when it starts
        {"pickup_end": NOW - HOUR},  # ends before it starts
        {"expires_at": NOW + HOUR},  # expires before pickup window closes
        {"pickup_start": NOW.replace(tzinfo=None)},  # no timezone
    ],
)
def test_donation_rejects_bad_values(overrides: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        DonationCreate(**donation_data(**overrides))


def test_read_schemas_accept_objects_with_attributes() -> None:
    # Stand-ins for SQLAlchemy objects; from_attributes reads plain attributes.
    donor_row = SimpleNamespace(**donor_data(), id=1, phone=None, contact_name=None, created_at=NOW)
    donation_row = SimpleNamespace(**donation_data(), id=7, status=DonationStatus.AVAILABLE, created_at=NOW)

    assert DonorRead.model_validate(donor_row).id == 1
    assert DonationRead.model_validate(donation_row).status is DonationStatus.AVAILABLE
