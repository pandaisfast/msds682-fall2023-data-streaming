# Lecture 2. Apache Kafka (Part 1.)

(Working In Progress)

Author: Jeremy Gu
  
## Basics of Apache Kafka 

Before delving into the intricate details of Apache Kafka, it's essential to lay down a broad overview. Starting with a holistic understanding of key concepts will keep us anchored and ensure that we don't get lost. Given that the version of Kafka we're using is continually evolving, we'll heavily reference official definitions and explanations to avoid redundancy. 

For this course, we'll be working with the latest Kafka version `3.6`. We encourage you to familiarize yourself with our recommended readings ahead of the class.

**Recommended Reading**:

- **Kafka Official Documentation** (Version: Kafka 3.6) at https://kafka.apache.org/documentation/. **Credits:** Any text in *italics* throughout this document is sourced directly from the Kafka Official Documentation.

**I. Introduction to Apache Kafka**

- **Definition:** Apache Kafka is an event streaming platform engineered for real-time collection, processing, storage, and data integration.
- **Officiial Explanation:** From https://kafka.apache.org/, *Kafka combines **three key capabilities** so you can implement your use cases for event streaming end-to-end with a single battle-tested solution:*

    - *To **publish** (write) and **subscribe** to (read) streams of events, including continuous import/export of your data from other systems.*
    - *To **store streams** of events durably and reliably for as long as you want.*
    - *To **process streams** of events as they occur or retrospectively*.

**II. Kafka as a Stream Processing Powerhouse**

- **Popularity:** Kafka reigns supreme as a leading streaming data platform in the industry, trusted and adopted widely.

- **Beyond Messaging:** While it provides an intuitive *message queue* interface, Kafka's essence lies in its append-only log-structured storage, transcending traditional messaging paradigms.
  
- **Events as Kafka’s Core:** 
    - Kafka is fundamentally an event log that chronicles occurrences.
    - These events portray things that have happened, not **directives** for **actions** to be undertaken.
    - An event has a key, value, timestamp, and optional metadata headers. Here's an example event from https://kafka.apache.org/:

```
Event key: "Alice"
Event value: "Made a payment of $200 to Bob"
Event timestamp: "Jun. 25, 2020 at 2:06 p.m."
```
  
- **Distributed DNA:** Kafka is innately distributed, fault-tolerant, and scales seamlessly from a single node to a massive thousand-node ensemble. From https://kafka.apache.org/, we have official definitions below.
    - *Kafka is a **distributed system** consisting of **servers** and **clients** that communicate via a high-performance TCP network protocol.*
    - **Servers**: *Kafka is run as a cluster of one or more servers that can span multiple data centers or cloud regions. Some of these servers form the storage layer, called **the brokers**. Other servers run Kafka Connect to continuously import and export data as event streams to integrate Kafka with your existing systems such as relational databases as well as other Kafka clusters.*
    - **Clients** *allow you to write distributed applications and microservices that read, write, and process streams of events in parallel, at scale, and in a fault-tolerant manner even in the case of network problems or machine failures.*
  
- **Data Guarantees:** A hallmark of Kafka is its assurance of data order preservation, crucial for deterministic real-time processing tasks.

- **Ecosystem Synergy:** Kafka seamlessly integrates with renowned streaming tools like Apache Spark, Flink, and Samza, broadening its capabilities.

**III. Main Concepts and Terminology**

- **What is an Event?** *An event records the fact that "something happened"*.

- **Kafka's Treatment of Events:** 
    - **Core Abstraction:** At its core, Kafka offers a distributed commit log, persistently storing events and ensuring their replication.
    - *Events are organized and durably stored in **topics**.*

- **Topics:** *A topic is similar to a folder in a filesystem, and the events are the files in that folder*.
    - *Topics are partitioned, meaning a topic is spread over a number of "buckets" located on different Kafka brokers* (storage layer).

- **Producers:** *Client applications that publish (write) events to Kafka.*

- **Consumers:** *Client applications that subscribe to (read and process) these events.*

    - *In Kafka, producers and consumers are fully decoupled and agnostic of each other, which is a key design element to achieve the high scalability that Kafka is known for.*

- **Source:** Refers to the origin or starting point where data is produced or ingested. In Kafka's ecosystem, a source would typically be a producer or an external system/service that sends data into Kafka. For instance, a database, an application, or any system that produces events could act as a source.

- **Sink:** Refers to the destination or endpoint where data is sent to or consumed. In Kafka, a sink would be the consumer or another data store where Kafka data is written. In the Kafka ecosystem, particularly with Kafka Connect, sinks are often connectors that stream data from Kafka to another system, such as a database, search index, or another type of data store.

**IV. A Peek into Kafka's Legacy**

- **Birth at LinkedIn:** Kafka was conceived at LinkedIn to cater to their internal streaming requisites. Now, as an Apache Foundation jewel, its adoption and growth are unparalleled.
  
- **Industry Usage** Titans like Uber, Apple, and Airbnb leverage Kafka for their mission-critical operations, a testament to its robustness.
  
- **Confluent's Contribution:**  After leaving LinkedIn, Kafka's creators founded Confluent. While Kafka remains under the Apache Software Foundation, Confluent significantly influences its development and provides extended tools and support.

- **The Literary Connection:** Kafka owes its name to Czech author *Franz Kafka*, reflecting its efficient nature of recording events.

**Exercise**

Which of the following messages is more indicative of an event-driven paradigm suitable for a system like Kafka?

A. `{"directive": "increase_volume", "level": 7}`

B. `{"event": "volume_changed", "previous_level": 6, "new_level": 7}`

C. `{"message": "Hello World", "recipient": "user123"}`


??? note

    **Answer**: B. `{"event": "volume_changed", "previous_level": 6, "new_level": 7}` 

    Explanation: Option B represents a change in state, capturing an "event" of the volume level changing, which aligns well with the event-driven paradigm. Option A seems more like a command or directive, while Option C is a generic message with no clear event or state change described.



## Examples of Managing Topics 

(Please read Lecture 2 PPT)

## Examples of Writing Producers 

(Please read Lecture 2 PPT)


---

## Example: Uber's Big Data Stack

<div class="result" markdown>

![Web_2](<../assets/index/uber big data Figure-1-5.png>){align=left width=600}
<div style="clear:both;"></div>
</div>

We have walked through basics of Kafka ecosystem. Next, I'd love to introduce an example of how to read industry engineering blogs that cover big data streaming systems. In the diagram above (Uber Eng Blog source[^1]), Uber leverages a diverse set of tools and technologies to manage its vast amount of data. This stack allows Uber to efficiently process, analyze, and act upon data generated from various sources like Rider App, Driver App, and other services. The diagram  illustrates the "Big Data Stack" used by Uber. The arrows between these components signify the flow of data and the relationships between various systems in the stack. Overall, the diagram provides a comprehensive view of how Uber might process, store, and analyze its big data. Let's break it down:

[^1]: Real-Time Exactly-Once Ad Event Processing with Apache Flink, Kafka, and Pinot (9/2021). https://www.uber.com/blog/presto-on-apache-kafka-at-uber-scale/. Note that Marmaray is an open source data ingestion and dispersal framework developed by Uber's Hadoop Platform team to move data into and out of their Hadoop data lake.

- **Sources**: At the leftmost part of the diagram, there are sources of data such as the "Rider App", "Driver App", "API/Services", and others. These represent the various applications and services from where data originates.
     - **Rider App**: Primarily for passengers, it collects data such as user locations, destinations, payment methods, and order histories.
     - **Driver App**: Tailored for drivers, it captures data points like driver locations, driving routes, order information, and income details.

- **Databases**: Beneath the source, you'll find different databases like "Cassandra", "Schemaless", and "MySQL". These are databases where Uber's raw data might be stored.

- **Ingestion**: The center of the diagram features an "Ingestion" process. This process is responsible for taking in data from the sources and feeding it into the big data systems. The systems involved in the ingestion process are:
  
    - **Kafka**: A real-time data streaming platform.
    - **Hadoop**: A distributed storage and processing framework.
    - **Amazon S3**: A cloud storage solution by Amazon.

- **Data Processing and Analytics**:

    - **Flink**: A stream-processing framework.
    - **Presto**: A distributed SQL query engine.
    - **Pinot**: A real-time distributed OLAP datastore.
    - **ELK**: Refers to the Elastic Stack, consisting of Elasticsearch, Logstash, and Kibana, used for searching, analyzing, and visualizing data in real-time.
     - **Spark**: A distributed data processing framework. Jobs, written using Spark's API, are divided into tasks and executed across cluster nodes. Its in-memory computing capability ensures rapid data processing.
     - **Hive**: Used for analytics reporting, it helps extract statistical data about orders, revenues, and user behaviors.

- **End Applications**: On the rightmost side, the diagram lists the potential applications or services that utilize the processed data. These include "Micro-Services", "Mobile App", "Streaming Analytics, Processing", "Machine Learning", "ETL, Applications Data Science", "Ad-hoc Exploration", "Analytics Reporting", and "Debugging".


<div class="result" markdown>

![Web_2](<../assets/index/uber Figure-2-2.png>){align=left width=600}
<div style="clear:both;"></div>
</div>


The subsequent diagram emphasizes Kafka's central role within Uber's tech stack. It facilitates numerous workflows, such as channeling event data from the Rider and Driver apps as a pub-sub message system, streaming analytics via Apache Flink, streaming database logs to downstream recipients, and ingesting assorted data streams into Uber's Apache Hadoop data lake. Considerable attention has been given to enhancing Kafka's efficiency, reliability, and user experience.

**Producers**:

- **Rider APP**: The application used by riders to book rides. It generates events like booking a ride, ride cancellations, rating a driver, etc. These events are produced and sent to Kafka clusters.
  
- **Driver APP**: The application used by drivers. It produces events like accepting a booking, starting a ride, ending a ride, and other driver-related activities. These events are subsequently channeled to Kafka clusters.
  
- **API/SERVICES**: Backend services or APIs produce events or logs. This could be any interaction with the system, error logs, or any backend process that needs to be logged or analyzed.

**Kafka Clusters**: The above apps and services generate event data that is produced/sent to the Kafka clusters.  The Kafka clusters sit at the core, tasked with receiving data from diverse producers and channeling this data to numerous consumers.

**Consumers**: 

- **Flink**: Apache Flink consumes events from Kafka for real-time stream processing. For instance, it might analyze real-time ride data for surge pricing decisions or traffic patterns.

- **Hadoop**: A big data storage and processing framework, it consumes data for long-term storage and batch processing. The data consumed here might be used for trend analysis or financial reporting. Note: Flink for real-time stream processing; Hadoop for batch processing and storage.

- **Apache Hive**: Operating over Hadoop, Hive consumes data to run SQL-like queries for data analysis.

- **Real-time Analytics, Alerts, Dashboards**: Systems that provide real-time insights, alerts, and visualization dashboards will consume the relevant data streams from Kafka.

- **Debugging**: Any system or tool used to monitor and debug issues will consume error logs or event data from Kafka.

- **Applications Data Science**: Data science applications that might be building models or running experiments will consume data from Kafka for their analytics and training needs.

- **Ad-hoc Exploration**: Any tool or system that needs to run exploratory analysis will consume the required datasets from Kafka.

- **Analytics Reporting**: Systems designed to report and visualize data will be consuming the processed or raw data from Kafka.

- **ELK (Elasticsearch, Logstash, Kibana)**: The ELK stack consumes log data for analytics and visualization. It helps in monitoring and troubleshooting.

--- 
