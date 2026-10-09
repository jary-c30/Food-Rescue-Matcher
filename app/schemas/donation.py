from datetime import datetime
from typing import Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

from app.core.enums import DonationStatus


class DonationCreate(BaseModel):
    donor_id: int
    description: str = Field(min_length=1, max_length=500)
    quantity_lbs: float = Field(gt=0)
    # AwareDatetime rejects times with no timezone, which would be ambiguous across regions.
    pickup_start: AwareDatetime
    pickup_end: AwareDatetime
    expires_at: AwareDatetime

    @model_validator(mode="after")
    def check_time_order(self) -> Self:
        if self.pickup_end <= self.pickup_start:
            raise ValueError("pickup_end must be after pickup_start")
        if self.expires_at < self.pickup_end:
            raise ValueError("expires_at must not be before pickup_end")
        return self


class DonationRead(DonationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: DonationStatus
    created_at: datetime


class DonationStatusUpdate(BaseModel):
    status: DonationStatus
