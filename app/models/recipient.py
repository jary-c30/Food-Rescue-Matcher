from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import OrganizationMixin


class Recipient(OrganizationMixin, Base):
    __tablename__ = "recipients"

    id: Mapped[int] = mapped_column(primary_key=True)
    capacity_lbs: Mapped[float | None] = mapped_column()
