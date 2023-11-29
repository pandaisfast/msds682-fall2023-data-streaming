# commands.py
from pydantic import BaseModel
from typing import Optional

# Commands for generating random data for the Kafka producers

class CreateTripCommand(BaseModel):
    # Command to create a fake trip record
    trip_id: Optional[str] = None  # Optional, as it can be generated
    driver_id: Optional[str] = None  # Optional, as it can be generated
    duration: Optional[str] = None  # Optional, as it can be generated
    mileage: Optional[str] = None  # Optional, as it can be generated
    pickup_location: Optional[str] = None  # Optional, as it can be generated
    destination_location: Optional[str] = None  # Optional, as it can be generated

class CreateDriverEarningCommand(BaseModel):
    # Command to create a fake driver earning record
    driver_id: Optional[str] = None  # Optional, as it can be generated
    trip_id: Optional[str] = None  # Optional, as it can be generated
    earnings_from_trip: Optional[float] = None  # Optional, as it can be generated

class CreateRiderCommand(BaseModel):
    # Command to create a fake rider record
    rider_id: Optional[str] = None  # Optional, as it can be generated
    trip_id: Optional[str] = None  # Optional, as it can be generated
    duration_estimate: Optional[str] = None  # Optional, as it can be generated
    initial_fare_estimate: Optional[float] = None  # Optional, as it can be generated
    final_adjusted_fare: Optional[float] = None  # Optional, as it can be generated
    payment_status: Optional[str] = None  # Optional, as it can be generated
    rating_to_driver: Optional[int] = None  # Optional, as it can be generated

class GenerateMultipleTripsCommand(BaseModel):
    number_of_trips: int