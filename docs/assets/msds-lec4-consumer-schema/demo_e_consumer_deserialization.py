# Schema Design 

## Lec 4 Demo: Serialization and Deserialization

"""Producer and consumer example demonstrating serialization in Kafka.

This script shows how to serialize data before producing to Kafka, and 
deserialize it after consuming from Kafka. 

It uses a RiderRequest dataclass which encapsulates the serialization logic,
keeping it separate from the Kafka producer/consumer code.

Key Functions:

- produce(): Serializes RiderRequest objects and publishes them to Kafka 

- consume(): Deserializes binary data from Kafka and reconstructs RiderRequest objects

- serialize() and deserialize(): Convert RiderRequest objects to and from binary data

The produce() function generates random rider data, serializes it using 
RiderRequest, and publishes it to Kafka. 

The consume() function subscribes to the same topic, deserializing the binary 
data back into RiderRequest objects.

"""


# Required libraries for concurrent execution, secrets management, and Kafka communication
import asyncio
from dotenv import load_dotenv
from confluent_kafka import Consumer, Producer, OFFSET_BEGINNING
from confluent_kafka.admin import AdminClient, NewTopic
import os
import sys
import random

#### Serialization and Deserialization

from datetime import datetime
from dataclasses import dataclass, field
import json

@dataclass
class RiderRequest:
    name: str
    lat: float
    long: float
    
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    request_date: str = field(init=False)
    request_hour: int = field(init=False)
    request_minute: int = field(init=False)

    def __post_init__(self):
        dt = datetime.fromisoformat(self.timestamp)
        self.request_date = dt.date().isoformat()
        self.request_hour = dt.hour
        self.request_minute = dt.minute

    def serialize(self):
        return json.dumps({
            "name": self.name,
            "timestamp": self.timestamp,
            "lat": self.lat,
            "long": self.long
        })

    @classmethod
    def deserialize(cls, json_data):
        data = json.loads(json_data)
        return cls(
            name=data["name"],
            timestamp=data["timestamp"],
            lat=data["lat"],
            long=data["long"]
        )

#### 

# Load the environment variables from the .env file
load_dotenv()

# Configuration Loader
def load_config():
    """Load Kafka configuration from environment variables."""
    return {
        'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
        'security.protocol': os.getenv('SECURITY_PROTOCOL'),
        'sasl.mechanisms': os.getenv('SASL_MECHANISMS'),
        'sasl.username': os.getenv('SASL_USERNAME'),
        'sasl.password': os.getenv('SASL_PASSWORD')
    }

# Kafka configuration is loaded globally for ease of use in other functions
config = load_config()

# Consumer Group ID for ensuring unique offset tracking
CONSUMER_GROUP_ID = os.getenv('CONSUMER_GROUP_ID', 'default-group-id')

## consumer 

def on_assign(consumer, partitions):
    """Callback executed when partitions are assigned. Sets partition offset to beginning."""
    for partition in partitions:
        partition.offset = OFFSET_BEGINNING
    consumer.assign(partitions)

## consumer 
async def consume(topic_name):
    """Asynchronously consume data from the specified Kafka Topic."""
    
    # Short delay before initiating the consumer
    await asyncio.sleep(2.5)

    # Configure consumer with Kafka settings and subscribe to the topic
    c = Consumer({
        **config,
        "group.id": CONSUMER_GROUP_ID,
        "auto.offset.reset": "earliest",
    })
    c.subscribe([topic_name], on_assign=on_assign)

    # Continuously poll for new messages in the topic
    while True:
        message = c.poll(1.0)
        if message is None:
            print("no message received by consumer")
        elif message.error() is not None:
            print(f"error from consumer {message.error()}")
        else:
            rider_request = RiderRequest.deserialize(message.value().decode('utf-8'))
            print(f"consumed message {message.key().decode('utf-8')}: {rider_request}")
        await asyncio.sleep(0.1)  # Brief pause to reduce CPU load


def main():
    """Entry point of the script. Starts producer-consumer tasks."""
    
    # Basic argument check for topic name
    if len(sys.argv) < 2:
        print("Usage: python3 script_name.py <TOPIC_NAME>")
        sys.exit(1)

    # Extract topic name from the arguments
    topic_name = sys.argv[1]
    client = AdminClient(config)
    
    # Start the main async function
    try:
        asyncio.run(produce_consume(topic_name)) 
    except KeyboardInterrupt as e:
        print("shutting down")

def delivery_report(err, msg):
    """Callback function to report the result of a produce operation."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

## producer 
async def produce(topic_name,config = config):
    """Asynchronously produce random person-location data into the specified Kafka Topic."""
    
    p = Producer(config)
    names = ["Alice", "Bob", "Charlie"]
    
    # Continuously produce messages to the topic
    while True:
        name = random.choice(names)
        lat = random.uniform(-90, 90)
        long = random.uniform(-180, 180)
        
        rider_request = RiderRequest(name=name, lat=lat, long=long)
        serialized_data = rider_request.serialize()

        message_key = f"rider-{name}".encode("utf-8") ## why we have this line?
        
        p.produce(topic_name, key=message_key, value=serialized_data, callback=delivery_report)
        p.poll(0.1)  # Poll to allow callbacks to be executed
        await asyncio.sleep(0.1)  # Brief pause to reduce CPU load

async def produce_consume(topic_name):
    """Concurrently run producer and consumer tasks using asyncio."""
    
    t1 = asyncio.create_task(produce(topic_name))  # Task for producing messages
    t2 = asyncio.create_task(consume(topic_name))  # Task for consuming messages
    await t1  # Wait for producer task to complete (infinite loop in this case)
    await t2  # Wait for consumer task to complete (infinite loop in this case)

if __name__ == "__main__":
    main()
    
# please run: python3 demo_e_consumer_deserialization.py consumer_example_deserialization