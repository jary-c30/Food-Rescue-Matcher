from pydantic import Field

from app.schemas.organization import OrganizationBase, OrganizationRead


class RecipientCreate(OrganizationBase):
    capacity_lbs: float | None = Field(default=None, gt=0)


class RecipientRead(OrganizationRead):
    capacity_lbs: float | None
