from pydantic import BaseModel, Field
from typing import Optional


#########################################################
#                                                       #
#       YOUR HOMEWORK BEGINS HERE IN THIS SCRIPT        #
#                                                       #
#########################################################


# Define the TripStreamModel class
class TripStreamModel(BaseModel):
    # Define a string field for trip_id
    trip_id: str
    # Add fields for driver_id (string), duration (string), mileage (string),
    # pickup_location (string), and destination_location (string)
    # Also, include optional fields for start_time and completion_time (both strings)

# Define the DriverEarningStreamModel class
class DriverEarningStreamModel(BaseModel):
    # Define fields for driver_id (string), trip_id (string), and earnings_from_trip (float)

# Define the RiderStreamModel class
class RiderStreamModel(BaseModel):
    # Define fields for rider_id (string), trip_id (string),
    # duration_estimate (string), initial_fare_estimate (float), final_adjusted_fare (float),
    # payment_status (string), and rating_to_driver (integer)
