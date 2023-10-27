# Lecture 3. Apache Kafka Part 2. Consumers


## Kafka Consumers Overview

Consumers read[^1] events from topics but don't remove them; topics remain immutable and durable.

Consumers subscribe[^2] to topics and read events from oldest to newest.


[^1]:Read: Refers to the action where a consumer retrieves or accesses events from a Kafka topic. These events remain in the topic even after being read, ensuring their availability for potential re-reads or access by other consumer applications.


[^2]:Subscribe: Refers to the act of a consumer indicating interest in one or more Kafka topics. Once subscribed, the consumer is eligible to receive events from those topics whenever they are produced. This sets the stage for the consumer to later read the events from the topics it has subscribed to.

---

### 

In Apache Kafka, each topic can be split into multiple partitions. Within each partition, messages (or events) are assigned a unique, sequential identifier called an "offset". 

When a consumer reads messages from a partition, it reads them in the order of their offsets, starting from the smallest (oldest) to the largest (most recent). This ensures that the consumer processes the messages in the same order they were produced and added to the partition. 

For instance, if a partition has messages with offsets 1, 2, 3, and so on, the consumer will first read the message with offset 1, then the message with offset 2, and continue in this sequential manner.


## Consumer Implementation



### Committing offsets

Committing offsets allows Kafka to track a consumer's position so it can resume from the last committed offset in case of failures. Let's dive into the concept of committing offsets in Kafka and the distinction between synchronous and asynchronous commits.

**Committing Offsets:**
When a consumer reads messages from a Kafka topic, it maintains a pointer, called an offset, to indicate up to which message it has read. "Committing" this offset means persistently storing this pointer so that, in case the consumer restarts, it can pick up right where it left off.

In Kafka, the default behavior for committing offsets is automatic and asynchronous. This means:

1. **Automatic**: Kafka's consumer will periodically commit the offset of messages that have been successfully returned by the `poll()` method, without the need for the application to explicitly ask for a commit. The frequency of this automatic commit is governed by the `auto.commit.interval.ms` setting.

2. **Asynchronous**: The commits are sent to the broker in the background, without blocking the consumer's processing. Asynchronous commits are generally faster because they don't wait for a response from the broker.

However, while this approach offers good performance, it may lead to at-least-once processing semantics. In the event of failures, some messages might be reprocessed since the commit might not have reached the broker before the failure occurred. For use cases that require exactly-once semantics, synchronous commits or manual offset management might be more appropriate.


**Synchronous vs. Asynchronous Commit:**

1. **Synchronous Commit:** The consumer sends a commit request and waits for the broker's acknowledgment. Only after receiving this acknowledgment does the consumer proceed to read more messages. This approach is safer but can be slower.
   
2. **Asynchronous Commit:** The consumer sends a commit request and immediately proceeds to read more messages without waiting for an acknowledgment from the broker. This approach is faster but carries a risk of data being re-read if the commit fails.

**Diagram for Asynchronous Commit:**

```
Consumer                  Kafka Broker
  |                           |
  | --- Read Msg (Offset 5)-->|
  | <---------Msg Received ---|
  |                           |
  | --- Async Commit 5 ------->|
  |                           |
  | --- Read Msg (Offset 6)-->|  (Before acknowledgment for Offset 5 commit is received)
  | <---------Msg Received ---|
  |                           |
  | <------ Ack Commit 5 ------|  (Ack received after the next message is read)
  |                           |
```

In the above diagram, after reading the message with offset 5, the consumer immediately sends an asynchronous commit for that offset and proceeds to read the next message without waiting for an acknowledgment. The acknowledgment for the Offset 5 commit comes back to the consumer after it has already started reading the next message (with Offset 6). This demonstrates the asynchronous nature of the commit process.

With asynchronous commits, there's a chance that even though the consumer has read and processed a message, if the commit fails and the consumer restarts, it might read the same message again.


**Diagram for Synchronous Commit:**

Here's the contrasted diagram showing the synchronous commit process:

```
Consumer                  Kafka Broker
  |                           |
  | --- Read Msg (Offset 5)-->|
  | <---------Msg Received ---|
  |                           |
  | --- Sync Commit 5 ------->|
  |                           |
  | <------ Ack Commit 5 -----|  (Consumer waits for this acknowledgment)
  |                           |
  | --- Read Msg (Offset 6)-->|  (Reading next message only after acknowledgment is received)
  | <---------Msg Received ---|
  |                           |
```

In the synchronous commit diagram, you can observe that the consumer reads the message with Offset 5 and commits it. It then waits for the acknowledgment of the commit before proceeding to read the next message (Offset 6). This waiting period ensures that the commit was successful, but can lead to slower message consumption compared to asynchronous commits.

### 

Here's a table that compares the terms "poll", "pull", "fetch", and some related concepts in the Kafka consumer context:

| Term       | Description                                                                                              | Kafka Relevance                                                                                                                                                     |
|------------|----------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Poll       | The action by which a Kafka consumer retrieves records from a Kafka topic.                               | In many Kafka client libraries, the method to get records from Kafka is called `poll()`. When invoked, it fetches records that haven't been read yet by the consumer. |
| Pull       | A mechanism where a consumer actively requests data from a provider, rather than having it pushed to them. | Kafka's consumption model is pull-based. This means consumers actively request (or "pull") data from brokers, rather than brokers pushing data to consumers.         |
| Fetch      | The retrieval of data.                                                                                   | In the Kafka context, "fetch" often refers to the actual retrieval of records from a broker in response to a `poll()` request. It's the mechanism behind the poll action.  |
| Consume    | The processing of fetched records.                                                                       | Once records are fetched by a Kafka consumer, they are "consumed", i.e., processed in some manner, such as storing, computing, or forwarding them.                      |
| Offset     | A sequential ID assigned to records as they arrive in a Kafka partition.                                 | Offsets let consumers track their position within a topic. It's crucial for ensuring records are processed reliably.                                                  |
| Commit     | Saving the last read offset, so that a consumer can pick up where it left off in case of restarts.       | Consumers can either automatically (default) or manually commit offsets. This tells Kafka up to which point records have been successfully consumed.                            |

This table provides a high-level comparison. Remember that while these terms have specific meanings within the Kafka context, they might be used differently in other systems or scenarios.

I also create workflow chart to explain the relationship between these terms in the Kafka consumer context.

```
    +--------+
    | Broker |
    +--------+
        |
        | 1. Pull (Initiated by Consumer)
        v
+-------------------+
| Consumer Requests |
| Records using     |
| the "poll()"      |
| method            |
+-------------------+
        |
        | 2. Fetch (Broker sends data in response to poll)
        v
+-------------------+
| Records are       |
| Fetched by the    |
| Consumer          |
+-------------------+
        |
        | 3. Consume (Consumer processes fetched records)
        v
+-------------------+
| Consumer Processes|
| and Uses Records  |
| (e.g. store, log) |
+-------------------+
        |
        | 4. Commit (Saving the last read offset)
        v
+-------------------+
| Offset is Committed|
| to Kafka to mark   |
| progress           |
+-------------------+
```

The process flows from top to bottom, depicting the typical flow of records from the Kafka broker to the consumer.


## Kafka Consumer Group

1. **Groups and Consumers**: Every Kafka reader (or "consumer") is part of a group.
2. **Unique ID**: Each group has a unique identifier called "group.id".
3. **Consumer Group**: A logical set of consumers that consume from the same topic.
4. **Same Logic, Different Partitions**: Each consumer within a group runs the same logic but consumes data from different partitions.
5. **Exclusive Partition Consumption**: Within a group, data from a single partition is consumed by only one consumer.
6. **Multiple Group Consumption**: Different consumer groups can independently consume the same topic without interfering with each other.
7. **Excess Consumers**: If the number of consumers in a group exceeds the number of partitions in a topic, the extra consumers remain idle as they have no data to consume.

Within the same consumer group (i.e., with the same `group.id`), it's generally recommended that all consumers have consistent settings. This ensures that all consumers in that group behave in a consistent manner, especially when it comes to handling offsets, rebalancing, and processing records. However, there might be some configurations that can differ, but fundamental configurations, especially those affecting processing semantics, should be consistent.


## Subscription

1. **Why use subscription in Kafka**:
   
      - **Topic Specification**: Consumers use subscriptions to specify which topics they want to consume from.
      
      - **Load Balancing**: For consumers in the same consumer group, Kafka automatically balances the load, ensuring each consumer reads from certain partitions, allowing parallel processing.
      
      - **Dynamic Topic Matching**: Consumers can subscribe to topics that match a certain pattern rather than specifying exact topics.

2. **Can we skip using subscription?**:

      - Without using subscription, a consumer wouldn't know from which topic to fetch data. However, Kafka allows "manual assignment" where consumers can be directly assigned to specific partitions without subscribing to the whole topic. This bypasses Kafka's automatic load-balancing, making developers manually manage it.
      
      - Manual assignment is useful in specific cases where precise control is needed, but generally, using subscriptions is more convenient as it automates partition assignment and balancing.

3. **Subscribing to Multiple Topics**: 
   
      - A consumer can listen to more than one topic using a pattern. When using patterns, follow the "regexp" format.
