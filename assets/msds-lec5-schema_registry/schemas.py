# schema.py

ride_request_schema = """
{
  "type": "record",
  "namespace": "com.uber",
  "name": "RideRequest",
  "fields": [
    {
      "name": "requestId",
      "type": "int",
      "doc": "Unique identifier for the ride request."
    },
    {
      "name": "userId",
      "type": "int",
      "doc": "Unique identifier for the user."
    },
    {
      "name": "pickupLocation",
      "type": {
        "type": "record",
        "name": "Location",
        "fields": [
          {
            "name": "latitude",
            "type": "double",
            "doc": "Latitude of the pickup location."
          },
          {
            "name": "longitude",
            "type": "double",
            "doc": "Longitude of the pickup location."
          }
        ]
      },
      "doc": "The structured geographic coordinates for the pickup location."
    },
    {
      "name": "pickupTime",
      "type": "string",
      "doc": "Time when the user wishes to be picked up."
    }
  ]
}
"""
