import enum


class DonationStatus(str, enum.Enum):
    AVAILABLE = "available"
    MATCHED = "matched"
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"
    EXPIRED = "expired"
