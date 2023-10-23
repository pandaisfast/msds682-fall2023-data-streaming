# Lecture 2. Apache Kafka Part 1. Basics and Producers

(Working In Progress)

Author: Jeremy Gu
  
## Basics of Apache Kafka 

Before delving into the intricate details of Apache Kafka, it's essential to lay down a broad overview. Starting with a holistic understanding of key concepts will keep us anchored and ensure that we don't get lost. Given that the version of Kafka we're using is continually evolving, we'll heavily reference official definitions and explanations to avoid redundancy. 

For this course, we'll be working with the latest Kafka version `3.6`. We encourage you to familiarize yourself with our recommended readings ahead of the class.

**Recommended Reading**:

- **Kafka Official Documentation** (Version: Kafka 3.6) at https://kafka.apache.org/documentation/. **Credits:** Any text in *italics* throughout this document is sourced directly from the Kafka Official Documentation.

### Introduction to Apache Kafka

- **Definition:** Apache Kafka is an event streaming platform engineered for real-time collection, processing, storage, and data integration.
- **Officiial Explanation:** From https://kafka.apache.org/, *Kafka combines **three key capabilities** so you can implement your use cases for event streaming end-to-end with a single battle-tested solution:*

    - *To **publish** (write) and **subscribe** to (read) streams of events, including continuous import/export of your data from other systems.*
    - *To **store streams** of events durably and reliably for as long as you want.*
    - *To **process streams** of events as they occur or retrospectively*.

### Kafka as a Stream Processing Powerhouse

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

### Main Concepts and Terminology

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

### A Peek into Kafka's Legacy

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

### Examples of Managing Topics 

(Please read Lecture 2 PPT)


## Producers 

### Examples of Writing Producers 

(Please read Lecture 2 PPT)


### Asynchronous Producer and Synchronous Producer

Below is a table that summarizes the use of `flush()`, `poll()`, and other methods for both asynchronous and synchronous Kafka producers:

| **Method/Action** | **Asynchronous Producer** | **Synchronous Producer** |
|--------------------|---------------------------|--------------------------|
| **flush()**       | **Used (After all messages)** - Called once after the loop has produced all messages to ensure that all of them have been delivered. It waits up to the given timeout for the delivery report callbacks to be triggered. | **Used (After each message)** - Called within the loop, after each `produce()`, to ensure that the current message is delivered and acknowledged before sending the next one. |
| **poll()**        | **Used** - Can be used within the loop or after it, primarily to trigger the delivery report callback and get feedback about the delivery status of messages. If used after the loop (as in the provided example), it will process delivery reports for all previously sent messages.| *Optional* - Not typically required in a purely synchronous producer since `flush()` waits for message acknowledgment. However, if you wanted feedback about delivery status after each message, you could use it. |
| **callback**      | **Used** - Callback functions (like `delivery_report`) are used to handle delivery reports asynchronously. They provide feedback about the delivery status of each message. | *Optional* - While callbacks can be used in synchronous producers, they're not as essential since you're relying on `flush()` to wait for acknowledgment. However, callbacks can provide more detailed information about the delivery. |

Remember that in real-world scenarios, you might find hybrid approaches based on the exact requirements of your application. The above distinctions are generalized to help you understand the conceptual differences between the two types of producers.

### Producer Congiuration

| Configuration         | Default Value  | Recommended Value | Description                                                                                              |
|-----------------------|---------------|---------------------|-------------------------------------------------------------------------------------------------------|
| `client.id`               | (none)           | (unique value)        | Identifier for the client in the Kafka cluster. Useful for tracking and debugging.                           |
| `retries`                   | 2147483647   | (depends on use case) | The number of retry attempts. A high default ensures durability but can be adjusted based on use case.       |
| `enable.idempotence` | false           | true                     | Ensures that messages are delivered exactly once by allowing retries without duplication.                       |
| `acks`                      | all or -1                 | all or -1            | The number of acknowledgments the producer requires the broker to receive before considering a message sent.    |
| `compression.type`     | none           | (depends on use case) | Type of compression to use (`none`, `gzip`, `snappy`, `lz4`, `zstd`). Chosen based on data and performance needs. |

[Source of Truth](https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md) is from the confluent github repo: https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md.


Based on [Apache Kafka Message Compression](https://www.confluent.io/blog/apache-kafka-message-compression/) published on 9/18/2023, here are the relevant passages that pertain to the topic-level compression and its precedence:

1. **Topic-Level Compression Precedence**:
   > "Typically, it works in the following manner when the producer is responsible for compression, and the topic’s compression.type is producer."
   
2. **Mismatch in Compression Settings**:
   > "Brokers always perform some amount of batch decompression in order to validate data."
   > "The following scenarios always require full payload decompression:
     The producer compresses batches (i.e., compression.type isn’t none), and the topic-level compression.type specifies a different codec or is uncompressed."
     

#### Choice of Compression Types

When decompression speed is critical, the following compression algorithms are commonly recommended in Kafka and other systems:

1. **Snappy**: Developed by Google, Snappy prioritizes speed over compression ratio. It doesn't compress as tightly as some other algorithms, but it decompresses very quickly.

2. **LZ4**: This is another compression algorithm that's designed for fast decompression speeds. In many benchmarks, LZ4 has been shown to be faster than Snappy, both in terms of compression and decompression, but with a slightly better compression ratio than Snappy.

Between the two, LZ4 is often **recommended** in Kafka for performance reasons, but the best choice can vary depending on the specific nature of the data and the requirements of the use case. Always consider benchmarking with your actual data to determine which one meets your needs best.

When network overhead is critical, meaning you want to minimize the amount of data sent over the network, you should opt for compression algorithms that provide the highest compression ratios, even if they are slower in terms of compression and decompression speed. Here are the common choices:

1. **gzip**: This is a widely-used compression algorithm that typically provides a good balance between compression ratio and speed. While it's not the fastest in terms of compression or decompression, it usually achieves smaller compressed sizes compared to faster algorithms like Snappy or LZ4.

2. **zstd (Zstandard)**: Developed by Facebook, zstd offers compression ratios comparable to gzip but at much faster speeds, especially in its higher compression levels. This makes zstd a great choice for scenarios where both network bandwidth and speed are concerns.

For maximum reduction in network overhead, you might lean toward gzip or zstd. zstd is often **recommended** over gzip due to its better speed while maintaining a similar, if not better, compression ratio. As always, it's beneficial to benchmark different algorithms with your actual data to determine the best fit for your specific needs.

#### client.id

The `client.id` is a configuration setting for Kafka clients (both producers and consumers). It's an identifier for the client in the Kafka cluster. This ID is used in logs, metrics, and for debugging purposes to identify the source of requests to the broker.

Having a unique `client.id` for each client allows administrators and developers to track requests, observe behavior, and troubleshoot issues more effectively because they can see which client is making which requests.

**Simple Example**:
Let's say you have a system with multiple Kafka producers, one that sends user activity data and another that sends system metrics. You can assign unique client IDs to each of them:

- For the producer that sends user activity data: `client.id=user-activity-producer`
- For the producer that sends system metrics: `client.id=system-metrics-producer`

Now, when you look at the logs or metrics from the Kafka broker, you can quickly identify which client (producer) is the source of a particular request or potential issue just by checking the `client.id`. This is especially helpful in environments with many clients interacting with a Kafka cluster.

#### Idempotence

When retries are enabled, enabling idempotence ensures messages remain in their intended order. For example, if messages A, B, and C are sent, but B fails initially while C succeeds, retries without idempotence might lead to an A, C, B order. With idempotence, the order A, B, C is preserved.


### Producer - Batch

A "batch" itself is a group of messages. 

1. **Batching Messages**: Kafka client libraries (producers) don't necessarily send every message individually. Instead, they batch multiple messages together into a single batch for efficiency reasons. This helps in reducing the overhead of network and I/O operations for each message, thus increasing throughput.

2. **Batches**: The term "batch" in Kafka's context refers to a collection of messages that are sent together in one go to a Kafka broker. Batching is a technique to improve application and network performance.

3. **Customizability**: The way messages are batched and sent — such as the size of the batch (`batch.size`), the time the producer waits before sending the batch (`linger.ms`), and the maximum size of a request (`max.request.size`) — are all customizable using producer configurations.


The belief that the Kafka producer sends messages one by one is incorrect. Here's why:

- **Batching**: The Kafka producer, including the Python client, doesn't send messages individually. Instead, it groups messages and sends them in batches for efficiency.
  
- **Configurable Settings**: The conditions for batching, like message count or elapsed time, are adjustable, allowing for performance tuning.
  
- **Compression**: Kafka can compress these batches, reducing bandwidth usage more effectively than compressing individual messages.
  
- **Optimized I/O**: Batching reduces the number of I/O operations, improving network and disk efficiency.


In the diagram below, each "Message" represents an individual message produced and ready to be sent. "[ Batch 1 ]" and "[ Batch 2 ]" represent groups of messages that the producer batches together based on certain conditions (like reaching a specific message count, size, or time limit). "Send Batch" represents the action of sending a batch of messages from the producer to the broker.

```
Producer                                        Broker
   |                                              |
   |---- Message 1 ----                           |
   |---- Message 2 ----                           |
   |---- Message 3 ----                           |
   |---- Message 4 ----                           |
   |                                              |
   |                                              |
   | Factors for batching:                        |
   |   - Count (e.g., 4 messages)                 |
   |   - Time (e.g., 500ms elapsed)               |
   |   - Size (e.g., nearing 1 GB)                |
   |                                              |
   |----[ Batch 1 ]---->|------ Send Batch ------>|
   |                    |                         |
   |---- Message 5 ----                           |
   |---- Message 6 ----                           |
   |                                              |
   |----[ Batch 2 ]---->|------ Send Batch ------>|
   |                                              |
```


**Performance Considerations**: 1) Throughput and 2) Overhead

- Batching is largely for performance reasons.
- In high-throughput applications, sending each message individually would result in significant network overhead.

Here is the **trade-off**: By waiting to accumulate messages, you can send fewer, larger batches, which can improve throughput. However, this could introduce a slight delay in individual message delivery times

Official Confluent Documentation:
https://docs.confluent.io/platform/current/installation/configuration/producer-configs.html

Batch Processing for Efficiency:
https://docs.confluent.io/kafka/design/efficient-design.html

Tutorial: How to optimize your Kafka producer for throughput:
https://developer.confluent.io/tutorials/optimize-producer-throughput/confluent.html



---
