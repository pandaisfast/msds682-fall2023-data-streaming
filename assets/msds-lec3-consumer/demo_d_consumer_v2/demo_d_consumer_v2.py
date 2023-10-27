# Required libraries for concurrent execution, secrets management, and Kafka communication
import asyncio
from dotenv import load_dotenv
from confluent_kafka import Consumer, Producer, OFFSET_BEGINNING
from confluent_kafka.admin import AdminClient, NewTopic
import os
import sys
import random

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
            print(f"consumed message {message.key()}: {message.value()}")
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

async def produce(topic_name,config = config):
    """Asynchronously produce random person-location data into the specified Kafka Topic."""
    
    p = Producer(config)
    names = ["Alice", "Bob", "Charlie"]
    
    # Continuously produce messages to the topic
    while True:
        name = random.choice(names)
        lat = random.uniform(-90, 90)
        long = random.uniform(-180, 180)
        message_key = f"rider-{name}".encode("utf-8")
        message_value = f"rider {name} requests a car at ({lat:.2f}, {long:.2f})".encode("utf-8")
        
        p.produce(topic_name, key=message_key, value=message_value, callback=delivery_report)
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
    
    # please run: python3 demo_d_consumer_v2.py consumer_example_v2