from pydantic import BaseModel
from typing import List

from entities import Location

# single record request
class CreateRideRequestCommand(BaseModel):
    userId: int
    pickupLocation: Location
    pickupTime: str

# If you expect to create multiple ride requests at once, you can use this:
class CreateRideRequestsCommand(BaseModel):
    rideRequests: List[CreateRideRequestCommand]
