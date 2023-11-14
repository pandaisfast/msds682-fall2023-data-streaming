#########################################################
#                                                       #
#       YOUR HOMEWORK BEGINS HERE IN THIS SCRIPT        #
#                                                       #
#########################################################

# Define the Avro schema for TripStreamModel
trip_stream_schema = """
{
  "type": "record",
  "name": "Trip",
  "fields": [
    # Example field: {"name": "trip_id", "type": "string"}
    # Add similar fields for driver_id, duration, mileage, pickup_location,
    # destination_location, start_time (optional), and completion_time (optional)
  ]
}
"""

# Define the Avro schema for RiderStreamModel
rider_stream_schema = """
{
  "type": "record",
  "name": "Rider",
  "fields": [
    # Add fields for rider_id, trip_id, duration_estimate, initial_fare_estimate,
    # final_adjusted_fare, payment_status, and rating_to_driver
  ]
}
"""

# Define the Avro schema for DriverEarningStreamModel
driver_earning_stream_schema = """
{
  "type": "record",
  "name": "DriverEarning",
  "fields": [
    # Add fields for driver_id, trip_id, and earnings_from_trip
  ]
}
"""
