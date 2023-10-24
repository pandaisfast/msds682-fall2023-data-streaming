"""
Kafka Topic Management API (v2)
Jeremy Gu

This script provides a FastAPI based microservice to interact with Kafka for topic management. 
It allows users to:
1. Create a Kafka topic based on configurations defined in a .env file.
2. Delete a specified Kafka topic.
3. Retrieve the status and metadata of a specified Kafka topic.

In the context of a Kafka topic:
- "leaders": It represents the broker ID that is the leader for a given partition of the topic. 
            A leader handles all read and write requests for the partition while the followers replicate the data.
- "configs": Configuration settings of a topic. This might include settings related to retention, partitioning, 
            and other topic-specific configurations.

Dependencies:
- FastAPI: To provide the web API interface.
- python-dotenv: To load environment variables from the .env file.
- kafka-python: To interact with the Kafka cluster.
"""

import logging
import os

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from kafka import KafkaAdminClient
from kafka.admin import NewTopic, NewPartitions
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError

# Loading environment variables from .env file
load_dotenv(verbose=True)

# Initializing FastAPI application
app = FastAPI()

# Set up logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

def get_kafka_client():
    """
    Create and return a KafkaAdminClient instance using environment variables.

    Returns:
        KafkaAdminClient: Configured KafkaAdminClient instance.
    """
    return KafkaAdminClient(
        bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
        security_protocol="SASL_SSL",
        sasl_mechanism=os.environ['SASL_MECHANISM'],
        sasl_plain_username=os.environ['SASL_USERNAME'],
        sasl_plain_password=os.environ['SASL_PASSWORD']
    )

@app.post("/topics/create")
async def create_topic():
    """
    Create a Kafka topic based on configurations from the .env file.

    Returns:
        dict: Response containing status of the topic creation.
    
    Raises:
        HTTPException: When topic already exists.
    """
    client = get_kafka_client()
    topic_name = os.environ['TOPICS_NAME']
    partitions = int(os.environ['TOPICS_PARTITIONS'])
    replicas = int(os.environ['TOPICS_REPLICAS'])

    topic = NewTopic(
        name=topic_name,
        num_partitions=partitions,
        replication_factor=replicas
    )

    try:
        client.create_topics([topic])
        return {"status": "Topic created successfully"}
    except TopicAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Topic already exists")
    finally:
        client.close()

@app.post("/topics/delete")
async def delete_topic():
    """
    Delete a Kafka topic based on configurations from the .env file.

    Returns:
        dict: Response containing status of the topic deletion.
    
    Raises:
        HTTPException: When topic is not found or any other unexpected error occurs.
    """
    client = get_kafka_client()
    topic_name = os.environ['TOPICS_NAME']

    # Step 1: Check if the topic exists
    existing_topics = client.list_topics()
    if topic_name not in existing_topics:
        client.close()
        raise HTTPException(status_code=400, detail="Topic not found")

    # Step 2 & 3: If topic exists, try to delete
    try:
        client.delete_topics([topic_name])
        return {"status": "Topic deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        client.close()

@app.get("/topics/status")
async def topic_status():
    """
    Get the status and metadata of a Kafka topic based on configurations from the .env file.

    Returns:
        dict: Contains various metadata fields about the topic.
    
    Raises:
        HTTPException: When topic is not found, metadata is unexpected or any other error occurs.
    """
    client = get_kafka_client()
    topic_name = os.environ['TOPICS_NAME']

    try:
        topics_metadata = client.describe_topics([topic_name]) 
        topic_metadata = topics_metadata[0]

        if 'partitions' not in topic_metadata:
            raise HTTPException(status_code=500, detail="Unexpected metadata format")
        
        partitions = [p['partition'] for p in topic_metadata['partitions']]
        replica_infos = [p['replicas'] for p in topic_metadata['partitions']]
        leaders = [p['leader'] for p in topic_metadata['partitions']]
        configs = topic_metadata.get('configs', {})

        result = {
            "name": topic_metadata['topic'],
            "partitions": partitions, 
            "replicas": replica_infos,
            "leaders": leaders,
            "configs": configs
        }

        return result

    except KeyError:
        raise HTTPException(status_code=404, detail="Topic not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        client.close()