# entities.py
# 
from pydantic import BaseModel, Field
from typing import Optional

class TripStreamModel(BaseModel):
    trip_id: str
    driver_id: str
    duration: str
    mileage: str
    pickup_location: str
    destination_location: str
    start_time: Optional[str] = Field(None, description="ISO format start time")
    completion_time: Optional[str] = Field(None, description="ISO format completion time")

class DriverEarningStreamModel(BaseModel):
    driver_id: str
    trip_id: str
    earnings_from_trip: float

class RiderStreamModel(BaseModel):
    rider_id: str
    trip_id: str
    duration_estimate: str
    initial_fare_estimate: float
    final_adjusted_fare: float
    payment_status: str
    rating_to_driver: int
