# Standard library imports for logging, operating system interactions, and type annotations
import logging
import os
from typing import List

# FastAPI framework for building APIs and handling HTTP requests and responses
from fastapi import FastAPI, HTTPException, status

# dotenv for loading environment variables from a .env file for configuration
from dotenv import load_dotenv

# Confluent Kafka client libraries for producing messages and managing Kafka topics
from confluent_kafka.admin import AdminClient, NewTopic  # Kafka administration (topics management)
from confluent_kafka import SerializingProducer  # Kafka producer with serialization capabilities
from confluent_kafka.serialization import StringSerializer  # Serializer for message keys
from confluent_kafka.schema_registry import SchemaRegistryClient  # For schema registry interactions
from confluent_kafka.schema_registry.avro import AvroSerializer  # Avro serializer for message values

# Libraries for generating fake data, compressing data, and creating unique identifiers
from faker import Faker  # Library to generate fake data (e.g., names, addresses)
import zlib  # Compression library for generating shorter unique IDs using CRC32
import uuid  # Library for generating unique identifiers

# Local modules containing application-specific classes and schemas
import schemas  # Avro schema definitions for Kafka message serialization
from entities import RideRequest, Location  # Data models representing business entities
from commands import CreateRideRequestCommand, CreateRideRequestsCommand  # Command models for API requests


# standard module for logging messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# 
load_dotenv(verbose=True)

app = FastAPI()

####
def get_kafka_config():
    return {
        'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS'],
        'security.protocol': os.environ['SECURITY_PROTOCOL'],
        'sasl.mechanisms': os.environ['SASL_MECHANISMS'],
        'sasl.username': os.environ['SASL_USERNAME'],
        'sasl.password': os.environ['SASL_PASSWORD'],
    }

@app.on_event('startup')
async def startup_event():
  client = AdminClient(get_kafka_config())
  topic = NewTopic(os.environ['TOPICS_NAME'],
              num_partitions=int(os.environ['TOPICS_PARTITIONS']),
              replication_factor=int(os.environ['TOPICS_REPLICAS']))
  try:
    futures = client.create_topics([topic])
    for topic_name, future in futures.items():
      future.result()
      logger.info(f"Create topic {topic_name}")
  except Exception as e:
    logger.warning(e)


def generate_request_id():
    # Generate a UUID and use a CRC32 hash to get a shorter integer
    return zlib.crc32(uuid.uuid4().bytes)

def make_producer() -> SerializingProducer:
    # Make a SchemaRegistryClient
    schema_registry_conf = {
        'url': os.environ['schema_registry_url'],
        'basic.auth.user.info': os.environ['basic_auth.user_info']
    }
    schema_reg_client = SchemaRegistryClient(schema_registry_conf)

    # Create AvroSerializer using the new RideRequest schema
    ## note: The Schema Registry is involved when the AvroSerializer serializes the data because it may need to fetch or register the schema.
    avro_serializer = AvroSerializer(
        schema_registry_client=schema_reg_client, # this is used to interact with the Confluent Schema Registry service.
        schema_str=schemas.ride_request_schema,  # the actual Avro schema (as a string) from schemas.ride_request_schema that defines the structure of the RideRequest data that will be serialized.
        to_dict=lambda ride_request, ctx: ride_request.dict(by_alias=True) #  This is a function used by the serializer to convert the RideRequest object into a dictionary format that matches the Avro schema. The 
        # In Avro serializer, the context (ctx) is an object that provides context for the serialization process.
    )

    # Create and return SerializingProducer with a simplified serializer configuration
    producer_conf = get_kafka_config()
    producer_conf.update({
        'acks': 'all',  # Ensures that the producer receives acknowledgment from all replicas
        'key.serializer': StringSerializer('utf_8'),
        'value.serializer': avro_serializer
    })

    return SerializingProducer(producer_conf)


# Define the producer callback for Kafka delivery reports
class ProducerCallback:
    def __init__(self, ride_request):
        self.ride_request = ride_request

    def __call__(self, err, msg):
        if err:
            logger.error(f"Failed to produce {self.ride_request}", exc_info=err)
        else:
            logger.info(f"Successfully produced {self.ride_request} to partition {msg.partition()} at offset {msg.offset()}")

# Endpoint for creating a single ride request
@app.post('/api/ride-request', status_code=status.HTTP_201_CREATED, response_model=RideRequest)
async def create_ride_request(ride_request: CreateRideRequestCommand):
    producer = make_producer()
    
    # Generate a requestId using a CRC32 hash of a UUID
    request_id = generate_request_id()
    
    ride_request_data = RideRequest(requestId=request_id, **ride_request.dict())

    # Produce the ride request to the Kafka topic
    producer.produce(
        topic=os.environ['TOPICS_NAME'],
        key=str(ride_request_data.userId), # Using userId as key (previously we used name), could be the requestId too
        value=ride_request_data,
        on_delivery=ProducerCallback(ride_request_data)
    )
    
    producer.flush()
    return ride_request_data

# Endpoint for creating multiple ride requests
@app.post('/api/ride-requests', status_code=status.HTTP_201_CREATED, response_model=List[RideRequest])
async def create_ride_requests(command: CreateRideRequestsCommand):
    producer = make_producer()
    ride_requests_data = []

    for ride_request_command in command.rideRequests:
        # Generate a requestId using a CRC32 hash of a UUID
        request_id = generate_request_id()
        
        ride_request_data = RideRequest(requestId=request_id, **ride_request_command.dict())
        ride_requests_data.append(ride_request_data)

        # Produce each ride request to the Kafka topic
        producer.produce(
            topic=os.environ['TOPICS_NAME'],
            key=str(ride_request_data.userId),  # Using userId as key (previously we used name), could be the requestId too
            value=ride_request_data,
            on_delivery=ProducerCallback(ride_request_data)  # Assuming ProducerCallback is defined elsewhere
        )

    # Flush the producer to ensure all messages are sent
    producer.flush()
    
    # Return the list of created ride requests
    return ride_requests_data


## uvicorn main:app --reload --port 8001


# curl -X 'POST' \
#   'http://localhost:8001/api/ride-request' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "userId": 12345,
#   "pickupLocation": {
#     "latitude": 37.7749,
#     "longitude": -122.4194
#   },
#   "pickupTime": "2023-11-03T10:00:00Z"
# }'



# curl -X 'POST' \
# 'http://localhost:8001/api/ride-requests' \
# -H 'accept: application/json' \
# -H 'Content-Type: application/json' \
# -d '{
# "rideRequests": [
#   {
#     "userId": 12345,
#     "pickupLocation": {
#       "latitude": 37.7749,
#       "longitude": -122.4194
#     },
#     "pickupTime": "2023-11-03T10:00:00Z"
#   },
#   {
#     "userId": 67890,
#     "pickupLocation": {
#       "latitude": 34.0522,
#       "longitude": -118.2437
#     },
#     "pickupTime": "2023-11-04T10:00:00Z"
#   }
# ]
# }'


from faker import Faker

fake = Faker()

@app.post('/api/ride-request/random', status_code=status.HTTP_201_CREATED, response_model=RideRequest)
async def create_random_ride_request():
    producer = make_producer()
    
    # Generate a requestId
    request_id = generate_request_id()

    # Generate fake data for the rest of the fields
    user_id = fake.random_int(min=1, max=10000)
    latitude = fake.latitude()
    longitude = fake.longitude()
    pickup_time = fake.iso8601(tzinfo=None, end_datetime=None)

    # Create a RideRequest instance with random data
    ride_request_data = RideRequest(
        requestId=request_id,
        userId=user_id,
        pickupLocation=Location(latitude=latitude, longitude=longitude),
        pickupTime=pickup_time
    )

    # Produce the ride request to the Kafka topic
    producer.produce(
        topic=os.environ['TOPICS_NAME'],
        key=str(ride_request_data.userId),
        value=ride_request_data,
        on_delivery=ProducerCallback(ride_request_data)
    )
    
    producer.flush()
    return ride_request_data

# curl -X POST "http://localhost:8001/api/ride-request/random" \
# -H "Accept: application/json"
