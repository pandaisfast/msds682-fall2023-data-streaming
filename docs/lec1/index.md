# Lecture 1. Streaming Processing

Author: Jeremy Gu

## Basics

Stream processing involves continuous calculations on constantly evolving data streams in real-time. Key aspects:

- **Data streams** are unbounded sequences (potentially endless) of data that can change in shape and size over time. 

- **Immutable data** - once in a stream, data is fixed and append-only. Existing data cannot be modified. Updates create new events.

- **Varying data rates** - streams can have bursts and lulls at uneven frequencies.

- **Low latency** - results are produced with minimal delays to enable real-time actions.

- **Fault tolerance** - streaming systems must handle failures gracefully.

## Streaming Data Characteristics 

- **Small data sizes** - events are typically less than 1 MB.

- **High throughput** - streams sustain high input data velocities. 

- **Irregular arrival patterns** - events arrive at inconsistent, uneven frequencies.

## Events in Streaming Data

**Events** capture immutable facts about something that happened in the system. 

- Example: GPS pings, Ads Clicks, purchases, sensor readings, etc.

**Event data** is dynamic, short-lived and not intended to be stored for a long duration, compared to traditional databases that overwrite older data.

Event producers emit facts without targeting specific consumers, unlike messaging queues which often have designated receivers.

**Note**: On updating existing record. To 'update' an event in an immutable system, one doesn't modify the existing event. Instead, a new event (or record) is appended to represent the change or the new state. Subsequent processing or reading systems can then consider the latest event as the 'current' state, effectively overriding the previous event.

!!! info

    We will cover more on **message queues** in [Additional Topics](1.1.md#message-queues). 

## Stream Processing and Batch Processing

In the realm of data engineering, batch and stream processing serve as two prominent paradigms. 

```
          +-----------------------------+
          |                             |
    +----->     Batch Processing        |
    |     |                             |
    |     +-----------------------------+
    |     |   Dataset 1   |   Dataset 2   | ... |   Dataset N   |
    |     +-----------------------------+---------------------+
    |      
    |      Time ------------------------->

    |      +-----------------------------+
    |      |                             |
    +------>   Streaming Processing      |
           |                             |
           +-----------------------------+
           | Event 1 | Event 2 | Event 3 | ... | Event N |
           +-----------------------------+---------------------+
          
           Time ------------------------->


```

### Comparison of Batch and Stream Processing

|                                  | **Batch Processing**                                                                                                 | **Stream Processing**                                                                                  |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| **Definition and Usage**         | Periodic analysis of unrelated groups of data. Historically common for data engineers.                                | Continuous analysis as new events are generated.                                                      |
| **Operation Frequency**          | Runs on a scheduled basis.                                                                                           | Runs at whatever frequency events (that may be uncertain) are generated.                                                      |
| **Duration & Storage**           | May run for a longer period of time and write results to a SQL-like store.                                             | Typically runs quickly, updating in-memory aggregates. Stream Processing applications may simply emit events themselves, rather than write to an event store. |
| **Data Analyzed**                | May analyze all historical data at once.                                                                             | Typically analyzes trends over a limited period of time due to data volume. Some batch jobs might only process a subset of the available data.                           |
| **Data Mutability**              | Typically works with mutable data and data stores.                                                                   | Typically analyzes immutable data and data stores.                                                    |
| **Examples**                     | (1) Aggregates the last hour of data every hour. This can help in capturing hourly user engagement metrics. (2) Results usually written to a SQL-like store, like aggregating monthly sales data for financial reporting. | (1) Real-time fraud detection based on latest transactions. (2) Social media trends based on real-time posts and interactions.                                    |
| **Pros**                         | (1) Data consumers receive updates periodically. (2) Can leverage all available data in the system.                     | (1) Outputs are up-to-date with the latest event. (2) Typically deals with immutable data, ensuring data consistency.                                           |
| **Cons**                         | (1) Best resolution of data is based on the batch interval. (2) Data might be mutable, meaning records can change between batches. This might lead to inconsistencies. | (1) Might lack full historical context. For instance, while it can capture sudden spikes in website traffic, it might not have the context of the overall daily or monthly trend. (2) Best suited for short-term trends. |
  
### Key Distinctions Between Batch and Stream Processing

| Key Characteristics                                  | **Batch Processing**                                                   | **Stream Processing**                                                                  |
|------------------------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| **Nature of Data Processed**                         | Operates on finite stored datasets.                                    | Handles near-infinite streams.                                                        |
| **Job Frequency**                                    | Runs jobs at discrete intervals.                                       | Continuous processing.                                                                |
| **Result Availability**                              | Results are available later.                                           | Results are available with low latency.                                                |
| **Focus & Accuracy**                                 | Emphasizes on completeness.                                            | Emphasizes on low latency but can offer accurate results with "exactly-once" semantics.|

**Note**: "Exactly-once semantics" means the system has mechanisms in place to ensure every piece of data is processed one time only.

```
Batch Processing:
                                                                                     
+---------+    +----------+    +----------+    +---------+   +---------+
| Raw     | -> | Extract  | -> | Transform| -> | Load    | ->| Database|
| Data    |    | & Clean  |    | & Model  |    | Process |   |         |
+---------+    +----------+    +----------+    +---------+   +---------+
              [Periodic intervals: e.g., daily, weekly]


Streaming Processing:
                                                                       
+---------+    +----------+     +--------+
| Event   | -> | Real-time| ->  |Output  |
| Stream  |    | Analysis |     |or DB   |
+---------+    +----------+     +--------+
              [Continuous: events processed as they arrive]

```
### General Notes
  - **Distinctions & Exceptions:** While we often categorize "batch processing" as periodic and "stream processing" as real-time, these are broad generalizations. In practice:
    - Some batch jobs may operate close to real-time.
    - Some stream processes might not be entirely real-time.
  - **Hybrid Systems:** Systems that integrate both batch and stream processing can harness the advantages of each approach, yielding more versatile and robust solutions.
  - **Interplay Between Batch and Stream:** Batch systems often produce events that are subsequently processed in real-time by stream systems. This synergy bridges the divide between historical data processing and real-time analytics.
    - It's essential to recognize the unique strengths of each approach. Neither makes the other redundant. In the realm of data engineering, batch and stream processing often complement each other, rather than serving as alternatives.

## Streaming Processing Application

Two key components: Streaming data store and Streaming calculations.

### E-commerce Example


```
+-------------------+          +------------------+          +---------------------+          +---------------------+
| Customer places   |   --->   | System generates |   --->   | Processes the       |   --->   | Inform Warehouse &  |
| an order          |          | an order ID      |          | payment             |          | Send Delivery Info  |
+-------------------+          +------------------+          +---------------------+          +---------------------+
                                                                                        |
                                                                                        v
                                                                                +---------------+
                                                                                | Notify User   |
                                                                                +---------------+

Outcome: Seamless integration of Kafka and stream processing applications for real-time e-commerce analytics.

```

When a customer places an order, the system of the e-commerce website will begin the tasks below:

- The system creates an order ID

- Process payment 

- Inform the warehouse for packaging

- Send delivery information to USPS or FedEx for shipping

The system creates an order, and the user receives a response that the order is being processed. 

**1. Streaming data store**: The e-commerce platform can use Kafka as a streaming data store to store event data such as users browsing, adding items to cart, and placing orders. Kafka stores data in time order and ensures data immutability.

**2. Stream processing calculation**: Perform real-time calculation of users' browsing volume in the past 1 hour and generate reports. Consume real-time event data from Kafka, perform counting, and generate browsing volume report events output to the database. This allows observing some issues, such as some goods being too popular leading to low inventory, or finding issues in certain steps (like payment) that requires engineer maintenance. Other use cases of stream processing calculation:

- Real-time tracking of most popular products (most clicked items)

- Real-time analysis of cart conversion rate (how many add to cart but do not purchase) 

- Real-time generation of purchase suggestions e.g. "Frequently bought together"

**Kafka** stores the input data, **stream processing applications** perform real-time processing and analysis on data consumed from Kafka, and output results. The combination enables real-time data processing for the e-commerce platform.

### Summary and Typical Data Processing Workflow

In summary, **Streaming Data** prioritizes immediacy. **Stored Data** prioritizes query-ability and depth. In many contexts, especially when distinguishing between "Stored" Data and Streaming data, it's generally implied that the data is stored in traditional, structured, and query-friendly systems, such as SQL-like databases.

| Parameter/Feature           | **Streaming Data (Real-time Data)**                                                                                                  | **Stored Data (SQL-like databases)**                                                                                                                                                                  |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Purpose**                 | Primarily used for real-time analytics and responses.                                                                                                             | Used for long-term storage and in-depth analysis.                                                                                                                                                     |
| **Typical Use Cases**       | - Analyzing user behaviors such as browsing, clicking, and purchasing in real-time.<br> - Making instantaneous decisions, e.g., adjusting product recommendations.   | - Product Details: Long-term storage of static info like product names, descriptions, categories, images, etc.<br> - Historical Pricing: Time series data storing price fluctuations for trend analysis.<br> - User Reviews: Long-term storage of feedback from customers.<br> - Order Information: Permanent record of each transaction's details. |
| **Characteristics**         | - Emphasizes immediacy and real-time actions.<br> - Data might be transient or archived after being processed.                                                    | - Emphasizes query-ability and historical context.<br> - Data is persistently stored for future retrieval and analysis.                                                                                                                                          |


**Typical Data Processing Workflow**:

1. **Real-time Stream Processing**: Streaming data undergoes real-time computations, providing insights like trending products.
2. **Data Storage**: Results from real-time computations are written to storage systems.
3. **In-depth Analysis**: Business intelligence systems query the stored data for comprehensive reports.
4. **Feedback Loop**: Analytical results are integrated back into the product or business strategies, completing a full cycle.


### Course Coverage

```
    +------------------+
    |    Kafka (MQ)    |
    +------------------+
               |
               v
    +--------------------------+
    | Stream Processing Apps   |
    +--------------------------+
               |
               v
    +------------------------+
    | Confluent KSQL & Faust  |
    +------------------------+
```

**Streaming Data Store** : We will focus on using **Kafka** in the course. **Kafka** is a **message queue system** mainly used for processing and transporting real-time data streams. It is designed as a publish-subscribe system to ensure data can be consumed in real-time by multiple consumers.

SQL stores like Cassandra will not be covered in our course. **Cassandra** is a **database** mainly used for long term data storage and querying. Although it supports stream data, its primary function is as a data storage system.


**Stream Processing Framework** - A comprehensive set of tools and utilities, often bundled together as a library or a platform, which facilitates the creation and management of Stream Processing Applications. This framework offers components that handle various aspects of stream processing, such as data ingestion, real-time analytics, state management, and data output, allowing developers to focus on the specific business logic of their application. Here is a list of Common Stream Processing Application Frameworks, as follows:

- **Confluent KSQL - will be focused on in the course**

- **Faust Python Library - will be focused on in the course**

- **Apache Flink - will be mentioned in the course**

- Apache Spark Structure Streaming - self-study needed

- Kafka Streams - self-study needed, especially for students proficient in Java

- Apache Samza - will not be covered in the course



## Examples of Using Data Streaming Services

### Shareride Requests

- **Input data:** Continuous stream of location data from riders' smartphones using GPS, details about driver locations, and availability.
  
- **Output:** Match rider requests with the most suitable driver in real time.
  
- **Problem statement:** To enable efficient and swift ride dispatching, process incoming location streams, and match the closest available driver to a requesting rider.
  
- **Models/Algorithms:** Could use the [Haversine formula](https://community.esri.com/t5/coordinate-reference-systems-blog/distance-on-a-sphere-the-haversine-formula/ba-p/902128#:~:text=All%20of%20these%20can%20be,longitude%20of%20the%20two%20points.) for calculating distances between geo-coordinates; a greedy assignment algorithm to match riders with drivers based on proximity and availability. (Optional reading: Approximate Nearest Neighbor (ANN) algorithms could be more efficient when dealing with a vast number of drivers and riders in close proximity.)

- **Streaming services:** Kafka for ingesting streams of rider requests and driver location updates; Spark Streaming for processing and assignment.

**Diagram and Example Data**

```
+---------------------+
| Rider's Smartphone  |
|                     |
|  - GPS Location     |
+----------+----------+
           |
           v
+----------+----------+
| Kafka (Data Ingest) |
+----------+----------+
           |
           v
+----------+----------+
| Spark Streaming App |
|                     |
|  - Haversine Calc.  |
|  - Greedy Matching  |
+----------+----------+
           |
           v
+---------------------+
|    Ride Dispatch    |
|                     |
|  - Matched Driver   |
+---------------------+
```

In this diagram:

- The "Rider's Smartphone" is continuously sending GPS location data.
- The data is ingested into the system using `Kafka`.
- `Spark Streaming` processes this data in real-time. It uses the Haversine formula to calculate distances and a greedy algorithm to match riders to drivers.
- The final result, a matched driver, is dispatched to the rider.

Here's an example of how the JSON data might look for various components in the ride-sharing example:

1. **Rider's Smartphone Data**:
   - Represents the continuous stream of location data from a rider's smartphone.

```json
{
  "rider_id": "12345",
  "timestamp": "2023-10-18T14:00:00Z",
  "location": {
    "latitude": 40.730610,
    "longitude": -73.935242
  },
  "ride_request": true
}
```

2. **Driver Location and Availability Data**:
   - Represents the details about driver locations and availability.

```json
{
  "driver_id": "98765",
  "timestamp": "2023-10-18T14:00:05Z",
  "location": {
    "latitude": 40.731000,
    "longitude": -73.934500
  },
  "availability": true
}
```

3. **Matched Ride Dispatch Data**:
   - Represents the output after processing the above inputs.

```json
{
  "ride_id": "67890",
  "rider": {
    "rider_id": "12345",
    "location": {
      "latitude": 40.730610,
      "longitude": -73.935242
    }
  },
  "driver": {
    "driver_id": "98765",
    "location": {
      "latitude": 40.731000,
      "longitude": -73.934500
    }
  },
  "estimated_arrival_time": "2023-10-18T14:05:00Z"
}
```

### Fraud Detection in Payments

- **Input data:** Continuous stream of financial transaction data, which includes purchases, withdrawals, and deposits.

- **Output:** Real-time alerts on suspicious or anomalous transactions.

- **Problem statement:** From a continuous stream of financial transactions, quickly identify and flag those that display patterns indicative of fraud.

- **Models/Algorithms:** Utilize unsupervised outlier detection models; clustering algorithms to identify and spotlight unusual patterns. Supervised learning techniques, such as Random Forests or Gradient Boosted Machines, could be employed when we have labeled data for fraudulent and non-fraudulent transactions. They can offer higher precision in anomaly detection compared to unsupervised methods. Also, mostly important process is to incorporate human feedback loop. 

- **Streaming services:** Kafka for ingesting transactional data streams; Flink for real-time anomaly and pattern detection.

**Diagram and Example Data**

```
  +----------------------+
  | Financial Transaction|
  |      Data Source     |
  +----------------------+
           |
           v
  +-------------------+
  |  Kafka Stream     |
  |    (Ingestion)    |
  +-------------------+
           |
           v
  +------------------+
  | Stream Processing|
  |   (Flink)        |
  +------------------+
           |
           |
  +--------v-------+
  |Machine Learning|
  |   Models (e.g. |
  |Random Forest)  |
  +----------------+
           |
           v
  +----------------------+
  | Real-time Fraud Alert|
  |  & Feedback System   |
  +----------------------+
```
The data flows from top to bottom:

1. **Financial Transaction Data Source** is where all transactions originate.
2. This data streams into a **Kafka Stream** for ingestion.
3. **Stream Processing** (with Apache Flink here) consumes this data, processes it in real-time, and applies various algorithms/models to detect potential fraud.
4. **Machine Learning Models**, like Random Forest, analyze patterns in the data to make predictions about potential fraud.
5. Detected anomalies are sent to a **Real-time Fraud Alert & Feedback System**, which could involve notifying account holders, bank agents, or flagging transactions for review.

Now, let's represent potential JSON data for this use case:

**Financial Transaction Data**:
   - Represents a single financial transaction event, such as a purchase.

```json
{
  "transaction_id": "abcd1234",
  "timestamp": "2023-10-18T14:10:00Z",
  "account_id": "A78901",
  "transaction_type": "purchase",
  "amount": 500.00,
  "currency": "USD",
  "merchant": {
    "name": "ElectronicsStore",
    "category": "Electronics",
    "location": {
      "latitude": 40.730610,
      "longitude": -73.935242
    }
  }
}
```

**Fraud Alert Data**:
   - Represents the output data after processing the transaction data.

```json
{
  "alert_id": "alert5678",
  "timestamp": "2023-10-18T14:10:05Z",
  "transaction_id": "abcd1234",
  "account_id": "A78901",
  "reason": "Unusual high amount",
  "action": "Flagged for review"
}
```

### Package Delivery Tracking

- **Input data:** Continuous GPS pings from delivery drivers' smartphones; shipment status updates.

- **Output:** Real-time updates on package delivery status and estimated time of arrival.

- **Problem statement:** Using a continuous stream of location data, frequently update the delivery status, and apply real-time optimizations to delivery routes.

- **Models/Algorithms:** Use rules-based algorithms to infer delivery status based on GPS data; real-time algorithms for optimizing delivery routes based on traffic and other constraints. Optimizing routes based on certain metrics (e.g. minimizing costs, maximizing speed, or other metrics) when there are multiple drops in bundles in a single trip.

- **Streaming services:** Kafka to ingest streams of GPS data and delivery updates; Spark Streaming for route analysis and optimization.

**Diagram and Example Data**

```
  +----------------------+
  | Package & GPS Data   |
  |     Data Source      |
  +----------------------+
           |
           v
  +-------------------+
  |  Kafka Stream     |
  |    (Ingestion)    |
  +-------------------+
           |
           v
  +--------------------+
  | Stream Processing  |
  |   (Spark Streaming)|
  +--------------------+
           |
           v
  +------------------+
  |Rules-based Status|
  |   Inference      |
  +------------------+
           |
           v
  +---------------------+
  |Route Optimization   |
  | Algorithms          |
  +---------------------+
           |
           v
  +----------------------+
  |Real-time Package     |
  |Status & ETA Updates  |
  +----------------------+
```

Here's the data flow:

1. **Package & GPS Data Source**: This is where the raw data (like GPS pings and shipment statuses) originates from the delivery drivers' devices.
2. This data then flows into a **Kafka Stream** for ingestion.
3. **Stream Processing** (using Spark Streaming in this case) takes this data and applies basic processing.
4. **Rules-based Status Inference** analyses the processed data to infer the delivery status based on the GPS data.
5. **Route Optimization Algorithms** take this inferred data, consider other variables (like traffic), and optimize the delivery routes.
6. The results from the above process are then sent to a system that provides **Real-time Package Status & ETA Updates** to the recipients or the main server.

Here are some potential JSON data structures:

1. **Package & GPS Data Source**:
```json
{
  "driver_id": "D12345",
  "timestamp": "2023-10-18T14:30:45Z",
  "gps_coordinates": {
    "latitude": 40.730610,
    "longitude": -73.935242
  },
  "shipment_status": "in_transit",
  "package_id": "PKG78910"
}
```

2. **Kafka Stream (Ingestion)**:
(This would look the same as the input data as Kafka is just ingesting the data.)
```json
{
  "driver_id": "D12345",
  "timestamp": "2023-10-18T14:30:45Z",
  "gps_coordinates": {
    "latitude": 40.730610,
    "longitude": -73.935242
  },
  "shipment_status": "in_transit",
  "package_id": "PKG78910"
}
```

3. **Stream Processing (Spark Streaming)**:
(The processed data might include more details, such as current speed or next destination.)
```json
{
  "driver_id": "D12345",
  "timestamp": "2023-10-18T14:30:45Z",
  "gps_coordinates": {
    "latitude": 40.730610,
    "longitude": -73.935242
  },
  "current_speed": "35 mph",
  "next_destination": {
    "latitude": 40.741895,
    "longitude": -73.989308
  },
  "shipment_status": "in_transit",
  "package_id": "PKG78910"
}
```

4. **Rules-based Status Inference**:
(This step infers the status based on the processed data, e.g., whether a driver has reached the destination.)
```json
{
  "driver_id": "D12345",
  "timestamp": "2023-10-18T14:35:00Z",
  "package_id": "PKG78910",
  "inferred_status": "delivered"
}
```

5. **Route Optimization Algorithms**:
(This data structure might focus on optimal route details.)
```json
{
  "driver_id": "D12345",
  "current_location": {
    "latitude": 40.730610,
    "longitude": -73.935242
  },
  "optimal_route": [
    {
      "latitude": 40.741895,
      "longitude": -73.989308
    },
    {
      "latitude": 40.752880,
      "longitude": -73.977326
    }
  ],
  "estimated_arrival": "2023-10-18T15:10:00Z"
}
```

6. **Real-time Package Status & ETA Updates**:
(This is the final data that would be sent to end-users.)
```json
{
  "package_id": "PKG78910",
  "current_status": "delivered",
  "driver_id": "D12345",
  "estimated_arrival": "2023-10-18T15:10:00Z"
}
```

Note: The timestamps and coordinates provided in these examples are arbitrary and are for illustrative purposes only. Actual data will vary based on real-world inputs.

### Other Considerations

- **Trade-offs**: Every streaming solution has to deal with the balance between latency (how fast data is processed) and throughput (how much data can be processed in a time frame). There's also accuracy, especially in ML where a faster prediction may be less accurate.

- **Stream Imperfections**: Data in the real world is messy. Streams can have missing data, or data can arrive out of sequence. Handling these imperfections requires strategies like watermarking or windowing.

- **Joining Streaming with Historical Data**: Often, the value from streaming data comes when it's combined with larger, historical datasets. Doing this efficiently is a challenge in stream processing.

- **Testing and Monitoring**: Streaming systems are complex and require sophisticated monitoring solutions. There should be mechanisms to ensure data integrity, monitor system health, and handle failures gracefully.

## Quiz

**Question 1. What is a key characteristic of data streams?**

- A) Bounded sequences 
- B) Immutable data
- C) Regular data arrival patterns
- D) Potentially unbounded sequences


**Question 2. What is a difference between streaming and batch data processing?**

- A) Streaming focuses on completeness while batch emphasizes speed 
- B) Streaming uses finite stored data while batch uses infinite streams
- C) Batch has higher latency than streaming
- D) Batch runs at scheduled intervals while streaming is continuous 


**Question 3. Which statement describes event data accurately?**

- A) Event data overwrites older data 
- B) Events directly target specific downstream consumers
- C) Events capture immutable facts about a system
- D) Events are typically larger than 1 MB in size


**Question 4. What does stream processing involve?**

- A) Discrete jobs running at regular intervals
- B) One-time calculations on finite data
- C) Continuous calculations on evolving data streams
- D) Loading data batches from databases


**Question 5. Which is NOT a streaming data characteristic?**

- A) Potentially high throughput 
- B) Strictly ordered arrival patterns
- C) Low latency results
- D) Small data sizes for individual events


**Question 6. What are benefits of using Streaming Processing Applications?**

(Open-ended question. Think about the themes like "use cases", "speed", "scalability", "storage", "architecture", etc.)


## Answers

**Question 1.**

D) Potentially unbounded sequences

Explanation: Data streams are potentially infinite and unbounded in size, rather than having a fixed length like bounded sequences. This endless nature is a core characteristic.

**Question 2.**

D) Batch runs at scheduled intervals while streaming is continuous  

Explanation: Batch processing runs at discrete scheduled intervals to process fixed datasets, while stream processing is continuous and operates on constantly evolving data streams.

**Question 3.**

C) Events capture immutable facts about a system

Explanation: Events are immutable facts about occurrences in a system, rather than overwriting older data like in databases. Events also emit facts indirectly rather than targeting specific downstream systems.

**Question 4.**

C) Continuous calculations on evolving data streams

Explanation: Stream processing continually performs calculations on live, updating data streams rather than finite stored data or intermittent batch jobs.

**Question 5.**

B) Strictly ordered arrival patterns

Explanation: Irregular and uneven arrival patterns are a characteristic of streaming data. Strictly ordered patterns are not typical as streams can have bursts and lulls.