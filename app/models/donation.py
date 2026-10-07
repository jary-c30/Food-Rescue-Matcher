import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.donor import Donor
from app.models.mixins import TimestampMixin


class DonationStatus(str, enum.Enum):
    AVAILABLE = "available"
    MATCHED = "matched"
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"
    EXPIRED = "expired"


class Donation(TimestampMixin, Base):
    __tablename__ = "donations"

    id: Mapped[int] = mapped_column(primary_key=True)
    donor_id: Mapped[int] = mapped_column(ForeignKey("donors.id"), index=True)
    description: Mapped[str] = mapped_column(String(500))
    quantity_lbs: Mapped[float] = mapped_column()
    pickup_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    pickup_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    # Stored as a string + CHECK constraint rather than a native Postgres enum,
    # because adding a value to a native enum later needs an awkward migration.
    status: Mapped[DonationStatus] = mapped_column(
        Enum(
            DonationStatus,
            native_enum=False,
            create_constraint=True,
            length=20,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=DonationStatus.AVAILABLE,
        index=True,
    )

    donor: Mapped[Donor] = relationship(back_populates="donations")
