# Demo #2A: Using Python to Consume Events

Author: Jeremy Gu

## Overview

**Demo Objective**:

- Learn to use python client  `confluent-kafka-python`
- We have introduced Producer and walked through Producer's python implementation. Now let's get a sense of how a Consumer works. 
  

In Demo #1, we have explored Confluent Cloud and Confluent CLI. You might be thinking, **"Where does Python fit into all of this?"** By the end of this demo, the student should be able to consume messages in a topic with Python client. For this demo, you'll be utilizing `confluent-kafka-python`, the Apache Kafka Python Client developed by Confluent. This client allows us to interface with Kafka using Python, enabling a more programmatic way to produce and consume events.

Recall that we have two options of **python client**: `confluent-kafka-python` and `kafka-python`.  

- [confluent-kafka-python](https://docs.confluent.io/kafka-clients/python/current/overview.html): presented in **Demo #2A**.
- [kafka-python](https://kafka-python.readthedocs.io/en/master/): presented in **Demo #2B**. 

Here's the comparison:

| Criteria         | [kafka-python](https://kafka-python.readthedocs.io/en/master/) (Demo #2B) | [confluent-kafka-python](https://docs.confluent.io/kafka-clients/python/current/overview.html) (Demo #2A) |
|------------------|------------------------|----------------------------------------|
| **Origin**       | Pure Python implementation. | Based on `librdkafka`, a high-performance C library for Kafka.  |
| **Performance**  | Generally lower performance. | Typically offers better performance due to `librdkafka`. |
| **Feature Support** | Supports core features but may lack some newer ones. | Usually quicker to support newer Kafka features. |
| **Maintenance**  | Maintained by Apache Kafka open-source community. | Maintained by Confluent, a major contributor to Kafka. |
| **Dependencies** | No external dependencies. | Requires `librdkafka`. |

In summary, for high performance and newer Kafka features, go for `confluent-kafka-python`. For a pure Python solution, choose `kafka-python`.

## Instructions

### Step 1. Setting up the environment

Begin by following the [getting-started installation guide](https://developer.confluent.io/get-started/python/) provided by Kafka.

**1.1. Create a Project Folder**
```bash
mkdir msds-demo2a
cd mkds-demo2a
```

**1.2. Set Up a Virtual Environment**
```bash
python -m venv .venv
```

**1.3. Activate the Virtual Environment**
```bash
source .venv/bin/activate
```

**1.4. Install Kafka Python Client Packages**
```bash

pip install pip --upgrade

pip install confluent-kafka
```

The version we are using is latest `2.2.0`. You might see something like `Successfully installed confluent-kafka-2.2.0`

### Step 2. CLI Setup

Run the following command to view the details of your Kafka cluster:

```
confluent kafka cluster describe
```

Details show up like below.

```
+----------------------+--------------------------------------------------------+
| Current              | true                                                   |
| ID                   | lkc-v1x365                                             |
| Name                 | cluster_0                                              |
| Type                 | BASIC                                                  |
| Ingress Limit (MB/s) | 250                                                    |
| Egress Limit (MB/s)  | 750                                                    |
| Storage              | 5 TB                                                   |
| Provider             | gcp                                                    |
| Region               | us-west4                                               |
| Availability         | single-zone                                            |
| Status               | UP                                                     |
| Endpoint             | SASL_SSL://pkc-lzvrd.us-west4.gcp.confluent.cloud:9092 |
| REST Endpoint        | https://pkc-lzvrd.us-west4.gcp.confluent.cloud:443     |
| Topic Count          | 1                                                      |
+----------------------+--------------------------------------------------------+
```
Note the value in the `Endpoint` field, e.g., `pkc-lzvrd.us-west4.gcp.confluent.cloud:9092`.


**Creating an API Key**:

To create an API key, execute:
```
confluent api-key create --resource {ID}
```

```

| API Key    | {.....} |
| API Secret | {.....} |

```
An API key and secret are needed to authenticate and interact with your Kafka cluster programmatically. The --resource {ID} is the cluster ID you've previously noted. This command will provide you an `API key` and `secret`. Keep them safe; you'll need them to authenticate your requests.

**Using the API Key**:

```
confluent api-key use {API Key} --resource {ID}
```

This tells the CLI to use the provided API key for authentication when interacting with the specified resource (Kafka cluster).


### Step 3. Configuration

**3.1 Create a file named `config.ini`**

The config.ini file serves as a configuration file for your Kafka consumer. Ensure the config.ini file safe and not sharing it, as it contains sensitive credentials.

To create the file in your current project directory, execute:

```
touch config.ini
```

Populate config.ini with the following content:

```config.ini
[default]
# Specify the Kafka broker addresses. This is typically the address of your Confluent Cloud cluster. < Endpoint >
bootstrap.servers=SASL_SSL://pkc-lzvrd.us-west4.gcp.confluent.cloud:9092

# Determine the security protocol. SASL_SSL indicates authentication using SASL and SSL for encryption.
security.protocol=SASL_SSL

# Specify the SASL mechanism used for authentication. PLAIN indicates plaintext authentication.
sasl.mechanisms=PLAIN

# The username for SASL/PLAIN authentication. Generally, this is a Confluent Cloud API key. < API Key >
sasl.username={.....}

# The password for SASL/PLAIN authentication. Generally, this is a Confluent Cloud API secret. < API Secret >
sasl.password={.....}

[consumer]
# It's essential to set a unique group ID for your application. Kafka uses this to manage the offsets of messages the consumer group has processed.
group.id=my_consumer_group

# This setting determines how to behave when the consumer starts and no committed offset is found.
# 'earliest' will make the consumer start from the beginning of the topic.
# Other possible values: 'latest' (start at the end), 'none' (throw an exception if no offset found).
auto.offset.reset=earliest
```

### Step 4. Write Python Consumer 


Create a new Python script named consumer.py:

```
touch consumer.py
```

You can copy and paste from the python script below.

- [consumer.py](../assets/msds-demo2a/consumer.py)
- [config.ini](../assets/msds-demo2a/config.ini)

**To Execute the Consumer Script:**

First, grant execute permissions to the script:


```bash
chmod u+x consumer.py

```

Then, run the script specifying the configuration file and topic:

```
./consumer.py config.ini demo1_free_text
```

Observations:

For best results, use two terminals:

- Terminal 1: Produce new events/messages.
- Terminal 2: Monitor messages being consumed by the Python script.


Once you see the messages being consumed, you can stop the consumer script in Terminal 2 using ctrl+C.

<div class="result" markdown>

![Web_2](<../assets/demo_or_exercise/demo2 - compare.png>){align=left width=600}

<div style="clear:both;"></div>
</div>

### Note: Offset in Consumer Setting

We will cover more in Lecture 3. Don't worry about this concept for now. 

When you run the consumer (`./consumer.py config.ini demo1_free_text`) for the first time and consume messages, Kafka keeps track of the last message you've read using a mechanism called "offsets". This allows Kafka to remember where each consumer left off and ensures that each message is processed once per consumer group.

When you run the consumer (`./consumer.py config.ini demo1_free_text`) again without producing new messages to the topic, the consumer starts from where it left off. Since there are no new messages after the last consumed message, you only see "Waiting...".

To better understand:

1. The first time you ran the consumer, it started from the earliest message (because you specified `auto.offset.reset=earliest`) and consumed all available messages in the topic.
   
2. The next time you ran the consumer, it started from where it last left off. If no new messages were produced to the topic in the meantime, the consumer has nothing new to read, and it will just wait for new messages.

**Summary**

- **earliest**: Useful for scenarios like reprocessing, data migration, or cluster migration where replaying data is essential.
- **latest**: Ideal for stateless applications or situations where only the latest data is of interest.
- **none**: Best suited for strict processing needs where starting without a valid offset is not acceptable.

