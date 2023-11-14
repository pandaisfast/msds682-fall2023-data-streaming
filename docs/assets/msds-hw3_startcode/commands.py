from pydantic import BaseModel
from typing import Optional


#########################################################
#                                                       #
#       YOUR HOMEWORK BEGINS HERE IN THIS SCRIPT        #
#                                                       #
#########################################################


# Define the CreateTripCommand class
class CreateTripCommand(BaseModel):
    # Define optional fields (all optional): trip_id, driver_id, duration, mileage,
    # pickup_location, destination_location (all should be of type Optional[str])

# Define the CreateDriverEarningCommand class
class CreateDriverEarningCommand(BaseModel):
    # Define optional fields for driver_id, trip_id (both Optional[str]),
    # and earnings_from_trip (Optional[float])

# Define the CreateRiderCommand class
class CreateRiderCommand(BaseModel):
    # Define optional fields for rider_id, trip_id (both Optional[str]),
    # duration_estimate (Optional[str]), initial_fare_estimate, final_adjusted_fare (both Optional[float]),
    # payment_status (Optional[str]), and rating_to_driver (Optional[int])

# Define the GenerateMultipleTripsCommand class
class GenerateMultipleTripsCommand(BaseModel):
    # Define a field for number_of_trips (int)
    number_of_trips: int
