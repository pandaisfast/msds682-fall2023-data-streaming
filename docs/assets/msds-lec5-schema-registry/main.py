"""
Kafka Producer Integration in FastAPI Application (v4 - with Confluent Kafka)

Objective:
To initialize a FastAPI application that generates random soccer player profiles and publishes them to a Kafka topic.

Description:
- On application startup, it loads necessary environment variables from a .env file.
- It creates a Kafka admin client to ensure the designated topic is available.
- Provides an API endpoint `/api/soccer_players` to:
  - Accept a specified count of soccer player profiles to be generated.
  - Generate profiles with unique IDs, random names, and assigned positions, along with ratings for speed, stamina, strength, and technique.
  - Serialize and publish each generated profile to a specified Kafka topic.
  - Return the list of generated profiles to the caller.
- Handles errors gracefully and logs significant events (if applicable).

Dependencies:
Requires FastAPI, confluent_kafka, python-dotenv, Faker, and Pydantic for operation.

Usage:
Ensure the .env file contains the correct Kafka configuration variables. The application is started by running a Uvicorn server with this module.

"""

# Standard Libraries
import os               # Accessing operating system functionality
import uuid             # Generating unique IDs
import random           # Random number and choice generation
from typing import List # Type hinting

# Third-Party Libraries
from dotenv import load_dotenv # Load environment variables from .env file
from faker import Faker        # Generate fake data
from fastapi import FastAPI    # Web framework

# Kafka Libraries
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

# Local Modules
from commands import CreatePeopleCommand   # Command format for creating entities
from entities import SoccerPlayer          # SoccerPlayer data model


# Load environment variables from .env file.
load_dotenv(verbose=True)

# Kafka configuration
kafka_config = {
    'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS'],
    'sasl.mechanisms': os.environ['SASL_MECHANISMS'],
    'security.protocol': 'SASL_SSL',
    'sasl.username': os.environ['SASL_USERNAME'],
    'sasl.password': os.environ['SASL_PASSWORD']
}
# topic = os.environ['TOPICS_NAME']

app = FastAPI()

# Startup event for the FastAPI application.
@app.on_event('startup')
async def startup_event():
    # Initialize a Kafka admin client.
    admin_client = AdminClient(kafka_config)

    # Attempt to create a Kafka topic.
    topic_list = [NewTopic(os.environ['TOPICS_NAME'], 
                           num_partitions=int(os.environ['TOPICS_PARTITIONS']), 
                           replication_factor=int(os.environ['TOPICS_REPLICAS']))]
    fs = admin_client.create_topics(topic_list)
    
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f"Topic {topic} created")
        except Exception as e:
            print(f"Failed to create topic {topic}: {e}")

# Utility function to create and return a Kafka producer instance.
def make_producer():
    producer = Producer(kafka_config)
    return producer

# Delivery report handler for produced messages
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# API endpoint to create and send random soccer player information to a Kafka topic.
@app.post('/api/soccer_players', status_code=201, response_model=List[SoccerPlayer])
async def create_soccer_players(cmd: CreatePeopleCommand):
    soccer_players: List[SoccerPlayer] = [] # This line is declaring a variable soccer_players inside the function. 
    
    faker = Faker()
    producer = make_producer()
    
    valid_positions = ["Forward", "Midfielder", "Defender", "Goalkeeper"]
    if cmd.position not in valid_positions:
        raise ValueError(f"Invalid position: {cmd.position}. Expected one of {valid_positions}.")

    for _ in range(cmd.count):
        soccer_player = SoccerPlayer(
            id=str(uuid.uuid4()), 
            name=faker.name(), 
            position=cmd.position,
            speed=random.randint(0, 10),
            stamina=random.randint(0, 10),
            strength=random.randint(0, 10),
            technique=random.randint(0, 10)
        )
        soccer_players.append(soccer_player)
        
        # Send the soccer player data to the Kafka topic.
        try:
            producer.produce(
                topic=os.environ['TOPICS_NAME'],
                key=str(soccer_player.position).lower(),
                value=soccer_player.json(),
                callback=delivery_report
            )
        except Exception as e:
            print(f"Error sending message to Kafka: {e}")

    producer.flush()  # Ensure all messages are sent.
    return soccer_players


# curl -X 'POST' \
#   'http://localhost:8001/api/soccer_players' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{"count": 5, "position": "Midfielder"}'