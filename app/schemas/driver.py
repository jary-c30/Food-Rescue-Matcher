from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class DriverCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    phone: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = None
    is_available: bool = True


class DriverRead(DriverCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
