from pydantic import BaseModel
from typing import Optional

class Location(BaseModel):
    latitude: float
    longitude: float

class RideRequest(BaseModel):
    requestId: Optional[int]  # requestId is now optional
    userId: int
    pickupLocation: Location
    pickupTime: str
