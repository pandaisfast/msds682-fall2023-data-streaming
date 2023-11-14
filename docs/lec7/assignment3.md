# Assignment 3: Building a Kafka-Integrated Application with FastAPI

**Due Date:** 11/22/2023 by 11:59pm

**Scoring:** Maximum of 15 points. Even with extra credits, the total score will not exceed 15 points.

**HW Submission:** [Canvas](https://usfca.instructure.com/courses/1617043/assignments/7369579)

**Pre-requisites:**

    - Completion of Demo #5B 
    - Understanding Coding Examples in Lec 5, 6, and 7. 
    - Creation of a Confluent Cloud account using your USF Gmail account (preferred).

## Objective

In this assignment, you will create a Python application that integrates Kafka for message processing using FastAPI. Your task involves setting up a Kafka producer and consumer, defining schemas for data serialization, and implementing a scheduler to manage message production.

This assignment is designed to be challenging and will require a good understanding of several advanced Python concepts. Good luck!

## Learning Outcomes

Upon completing this assignment, you should be able to:

    1. Set up and configure Kafka in a Python application.
    2. Define and use Pydantic models for data validation and serialization.
    3. Implement Avro schemas for Kafka message serialization.
    4. Create and manage a Kafka producer in a FastAPI application.
    5. Implement asynchronous tasks using two different approaches.

## Resources

You will be provided with a starter code package that includes several Python files. Familiarize yourself with the structure and purpose of each file as outlined in the assignment's introduction.

### Structure of the helper code

```
Directory .
├── .env                # Holds configuration for Kafka and Schema Registry connections.
├── commands.py         # Pydantic models for request data validation.
├── entities.py         # Pydantic models for core data structures.
├── producer.py         # FastAPI setup, endpoints, and Kafka producer logic.
├── requirements.txt    # Lists Python dependencies for the project.
├── schemas.py          # Avro schema definitions for message serialization.
├── scheduler1.py       # Manages request timing using AsyncIOScheduler.
└── scheduler2.py       # Sends requests in a loop using asyncio.
```

## Tasks

### 1. Environment Setup
- Follow the detailed instructions provided to set up your working environment, including Confluent Cloud, Python virtual environment, and package installation.

### 2. Model and Schema Definitions
- Complete the `entities.py`, `commands.py`, and `schemas.py` files. 
- Ensure that your Pydantic models and Avro schemas are aligned and accurately reflect the structure required for the Kafka messages.

### 3. Kafka Producer Implementation
- In the `producer.py` file, implement the various functions and endpoints necessary for Kafka message production.
- Your implementation should handle message serialization, error handling, and successful message delivery acknowledgment.

### 4. Scheduler Implementation
- Run either of the two different schedulers (`scheduler1.py` and `scheduler2.py`) for managing message production.
- Compare and analyze the performance and characteristics of both schedulers as per the guidelines provided.

### 5. Testing and Validation
- Test your application thoroughly to ensure that all components are working as expected.
- Validate that messages are correctly produced and consumed by Kafka, and that the data conforms to the defined schemas.

## Submission Guidelines

- Submit all your files in a zipped folder. Ensure the folder structure is organized and the files are easy to navigate.
- Make sure that your code is well-commented, clean, and adheres to best practices for readability and maintainability.
- Your screenshots should clearly demonstrate that each part of the application is functioning as expected.
- For extra credit, ensure that `Consumer.py` is robust and handles edge cases gracefully.

## Deliverables

Submit the following components (15 points plus extra 5 points).

- **Core Implementation**

    **Code Submission (5pts)**: Submit completed Python files (`entities.py`, `commands.py`, `schemas.py`, `producer.py`). 

- **Screenshots Demonstrating Functionality**
   
    (a) **FastAPI Application (5pts)**: Take a screenshot showing the FastAPI application running in the terminal.

    (b) **Scheduler Execution (5pts)**: Take a screenshot of either `scheduler1.py` or `scheduler2.py` running in the terminal.

- **Extra Credit Challenge**

    **Consumer Implementation (5pts)**: Create a `Consumer.py` that consumes three streams, joins them based on `trip_id`, and produces to a new topic `hw.fake.joinedstreams`. Include a screenshot of this script running in your submission.
