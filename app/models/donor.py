from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import OrganizationMixin


class Donor(OrganizationMixin, Base):
    __tablename__ = "donors"

    id: Mapped[int] = mapped_column(primary_key=True)

    donations: Mapped[list["Donation"]] = relationship(back_populates="donor")  # noqa: F821
