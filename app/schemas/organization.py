from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrganizationBase(BaseModel):
    """Fields shared by donors and recipients. Limits match the database column sizes."""

    name: str = Field(min_length=1, max_length=200)
    address: str = Field(min_length=1, max_length=300)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    phone: str | None = Field(default=None, max_length=30)
    contact_name: str | None = Field(default=None, max_length=200)


class OrganizationRead(OrganizationBase):
    # from_attributes lets Pydantic read values straight off a SQLAlchemy object.
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
