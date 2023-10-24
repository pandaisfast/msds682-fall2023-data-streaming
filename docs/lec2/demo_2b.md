# Demo #2A: Kafka Topic Management with FastAPI and Python: A Tutorial

Author: Jeremy Gu

**Demo Objective**:

- Learn to use python client  `kafka-python`
- (Optional) Learn basics of `FastAPI`

Managing Kafka topics can become challenging as your data needs grow. This tutorial offers a solution by creating a microservice using `kafka-python` and `FastAPI`, allowing for streamlined topic management. By the end, you'll be able to create, view, and delete Kafka topics with ease.

Reference: [`kafka-python` Documentation](https://kafka-python.readthedocs.io/en/master/)

## Why FastAPI?

FastAPI provides a rapid way to build web APIs. With automatic interactive API documentation and built-in OAuth and JWT, it's both developer-friendly and robust enough for production use. When combined with Kafka's powerful streaming capabilities, it becomes a potent tool for managing topics.

## Instructions

**Prerequisites:**

1. Familiarity with Python programming.
2. Basic understanding of Kafka.
3. Python environment setup (recommend using `virtualenv`).
4. Installed `fastapi`, `uvicorn`, `python-dotenv`, and `kafka-python` packages.

**Step 1: Setup Environment**

Create a directory.

```
mkdir msds-demo2b
cd msds-demo2b
```

Begin by setting up a Python virtual environment to keep our dependencies isolated:
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

To set up the environment, install the necessary packages. If you have a requirements.txt file, you can use it. Otherwise, you can manually install the packages using the following command:
```bash
$ pip install fastapi uvicorn python-dotenv kafka-python
```

**Step 2: Configuration Management with .env**

Our demo uses environment variables to manage Kafka configurations. Create a `.env` file in your project directory. Referring to `config.ini` from the previous demo could be helpful. In this demo, we introduce `python-dotenv` as an alternative solution to store secrets instead of `config.ini`.

Note: When using Git, ensure that both `.env` and `.venv` folders are added to your `.gitignore` file. Especially the `.env` file, as it contains sensitive configuration data, should never be committed to source control.

```
BOOTSTRAP_SERVERS=your_kafka_bootstrap_servers
SASL_MECHANISM=your_sasl_mechanism
SASL_USERNAME=your_sasl_username
SASL_PASSWORD=your_sasl_password
TOPICS_NAME=your_topic_name
TOPICS_PARTITIONS=your_partition_count
TOPICS_REPLICAS=your_replica_count
```
Replace placeholders with actual Kafka configurations.

Note: Both the `.env` and `.venv` folder can be gitignored and should not be committed to source control.

**Step 3: Code Overview**

We have three main Kafka functionalities within [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/). If you need help, please refer to the Appendix with the Scripts used in the demo. 

1. Create a Kafka topic at the app starting up. 
2. Delete a Kafka topic.
3. Get the status of a Kafka topic.

For all operations, we make use of the `KafkaAdminClient` provided by `kafka-python`.

The `main.py` structure looks like below. 
```py
"""
Kafka Topic Management API (v2)
Jeremy Gu (Scaffolded Version)

This script provides a FastAPI based microservice to interact with Kafka for topic management. 

Your task:
- Complete the missing parts of the code and test the endpoints.
"""

# Required imports
import logging
import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError

# Loading environment variables from .env file
load_dotenv(verbose=True)

# Initializing FastAPI application
app = FastAPI()

# Set up logging (no changes needed here)
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

def get_kafka_client():
    """
    Create and return a KafkaAdminClient instance using environment variables.

    TODO:
    - Create a KafkaAdminClient with the required configurations.
    """
    # Fill in the required parameters from the environment variables
    return KafkaAdminClient(
        bootstrap_servers=None,  # TODO: Get from environment variable
        security_protocol=None,  # TODO
        sasl_mechanism=None,    # TODO
        sasl_plain_username=None,  # TODO
        sasl_plain_password=None   # TODO
    )

@app.post("/topics/create")
async def create_topic():
    """
    Create a Kafka topic based on configurations from the .env file.

    TODO:
    - Extract topic configurations from the environment.
    - Use KafkaAdminClient to create the topic.
    """
    client = get_kafka_client()

    # TODO: Get topic configurations (name, partitions, replicas) from environment variables

    topic = NewTopic(
        name=None,           # TODO
        num_partitions=None,  # TODO
        replication_factor=None   # TODO
    )

    # Try creating the topic
    try:
        # TODO: Use client to create the topic
        pass
    except TopicAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Topic already exists")
    finally:
        client.close()

@app.post("/topics/delete")
async def delete_topic():
    """
    Delete a Kafka topic based on configurations from the .env file.

    TODO:
    - Check if the topic exists.
    - Delete the topic if it exists.
    """
    client = get_kafka_client()

    # TODO: Get topic name from environment variables

    # Check if the topic exists
    existing_topics = client.list_topics()
    if None:  # TODO: Replace None with the condition to check if topic exists
        # TODO: Use client to delete the topic
        pass
    else:
        raise HTTPException(status_code=400, detail="Topic not found")
    finally:
        client.close()

@app.get("/topics/status")
async def topic_status():
    """
    Get the status and metadata of a Kafka topic based on configurations from the .env file.

    TODO:
    - Fetch the topic's metadata.
    - Extract relevant information for the response.
    """
    client = get_kafka_client()

    # TODO: Get topic name from environment variables

    try:
        # TODO: Fetch the topic's metadata using the client

        # TODO: Construct the result with relevant topic metadata
        result = {
            "name": None,  # TODO
            "partitions": None,  # TODO
            "replicas": None,  # TODO
            "leaders": None,  # TODO
            "configs": None   # TODO
        }

        return result
    except KeyError:
        raise HTTPException(status_code=404, detail="Topic not found")
    finally:
        client.close()

# NOTE: Don't forget to handle exceptions properly where necessary!

```


**Step 4: Run the FastAPI Application**
To run our FastAPI application, we need to use `uvicorn`. In the terminal, navigate to the directory containing your FastAPI code (from the provided code in the previous sections) and run:
```bash
$ uvicorn filename:app --reload
```

Or, run `uvicorn filename:app --reload --port 8001` if 8000 is already occupied.

Replace `filename` with the name of your Python file (without the `.py` extension).

**Step 5: Using the FastAPI Endpoints**

Navigate to http://127.0.0.1:8000/docs to access the FastAPI documentation interface. 

1. **Creating a Kafka Topic:**
   Use a tool like `curl` or any API testing tool to hit the endpoint:
   ```bash
   $ curl -X 'POST' 'http://127.0.0.1:8000/topics/create' -H 'accept: application/json'
   ```
   If successful, you'll receive a response indicating the topic was created. The topic name is defined in the `.env` file.

2. **Deleting a Kafka Topic:**
   Similarly, to delete a topic:
   ```bash
   $ curl -X 'POST' 'http://127.0.0.1:8000/topics/delete' -H 'accept: application/json'
   ```

3. **Checking Topic Status:**
   To retrieve the status of a Kafka topic:
   ```bash
   $ curl -X 'GET' 'http://127.0.0.1:8000/topics/status' -H 'accept: application/json'
   ```

## Future Steps
In this tutorial, we've walked through the process of setting up a FastAPI application to manage Kafka topics using a Python client. This approach offers a programmatic way to manage Kafka topics and can be integrated into larger systems or web interfaces. 

This is a very simple touch on FastAPI and Web Application in the course. Mastering FastAPI and Kafka offers a competitive edge for data engineers and app developers. FastAPI allows swift API development, and Kafka handles real-time data streaming. Learning these tools enhances your skill set and positions you well in the evolving tech landscape. While there's a learning curve, the practical benefits of integrating FastAPI and Kafka are substantial and worth the effort.


## Appendix. Scripts used in the demo

- [.env](../assets/msds-demo2b/.env)
  
- [config.ini](../assets/msds-demo2b/config.ini): We won't need this file as we're using `.env`.
  
- [main.py](../assets/msds-demo2b/main.py)
  
- [requirements.txt](../assets/msds-demo2b/requirements.txt)
