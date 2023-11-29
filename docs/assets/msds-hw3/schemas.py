# schema.py

# Trip Stream Schema

## day, date, month, hour, city, state, ....

trip_stream_schema = """
{
  "type": "record",
  "namespace": "com.example",
  "name": "Trip",
  "fields": [
    
    {"name": "trip_id", "type": "string"},
    {"name": "driver_id", "type": "string"},
    {"name": "duration", "type": "string"},
    {"name": "mileage", "type": "string"},
    {"name": "pickup_location", "type": "string"},
    {"name": "destination_location", "type": "string"},
    {"name": "start_time", "type": ["null", "string"], "default": null},
    {"name": "completion_time", "type": ["null", "string"], "default": null}
  ]
}
"""

# Rider Stream Schema
rider_stream_schema = """
{
  "type": "record",
  "namespace": "com.example",
  "name": "Rider",
  "fields": [
    {"name": "rider_id", "type": "string"},
    {"name": "trip_id", "type": "string"},
    {"name": "duration_estimate", "type": "string"},
    {"name": "initial_fare_estimate", "type": "double"},
    {"name": "final_adjusted_fare", "type": "double"},
    {"name": "payment_status", "type": "string"},
    {"name": "rating_to_driver", "type": "int"}
  ]
}
"""

# Driver Earning Stream Schema
driver_earning_stream_schema = """
{
  "type": "record",
  "namespace": "com.example",
  "name": "DriverEarning",
  "fields": [
    {"name": "driver_id", "type": "string"},
    {"name": "trip_id", "type": "string"},
    {"name": "earnings_from_trip", "type": "double"}
  ]
}
"""

# Joined Stream Schema
joined_stream_schema = """
{
  "type": "record",
  "namespace": "com.example",
  "name": "JoinedStream",
  "fields": [
    {"name": "trip_id", "type": "string"},
    {"name": "trip_info", "type": {
      "type": "record",
      "name": "TripInfo",
      "fields": [
        {"name": "duration", "type": "string"},
        {"name": "duration_estimate", "type": "string"},
        {"name": "mileage", "type": "string"},
        {"name": "pickup_location", "type": "string"},
        {"name": "destination_location", "type": "string"}
        {"name": "start_time", "type": ["null", "string"], "default": null},
        {"name": "completion_time", "type": ["null", "string"], "default": null}
      ]
    }},
    {"name": "rider_info", "type": {
      "type": "record",
      "name": "RiderInfo",
      "fields": [
        {"name": "rider_id", "type": "string"},
        {"name": "initial_fare_estimate", "type": "double"},
        {"name": "final_adjusted_fare", "type": "double"},
        {"name": "payment_status", "type": "string"},
        {"name": "rating_to_driver", "type": "int"}
      ]
    }},
    {"name": "driver_earning_info", "type": {
      "type": "record",
      "name": "DriverEarningInfo",
      "fields": [
        {"name": "driver_id", "type": "string"},
        {"name": "trip_id", "type": "string"},
        {"name": "earnings_from_trip", "type": "double"}
      ]
    }}
  ]
}
"""