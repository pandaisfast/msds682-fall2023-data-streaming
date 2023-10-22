**Assignment #1: Kafka Producers Performance Analysis**

**Due Date:** 10/28/2023 by 11:59pm

**Scoring:** Maximum of 10 points. Even with extra credits, the total score will not exceed 10 points.

**Pre-requisites:**

- Completion of Demo #1
- Understanding Coding Examples in Lec 2. 
- Creation of a Confluent Cloud account using your USF Gmail account (preferred).

---

**Problem 1: Confluent Cloud Producers Performance Analysis**

**Objective:**  
You will set up your cluster in the Confluent Cloud, use both asynchronous and synchronous Kafka producers, and compare their performance.

**Tasks:**

1. **Confluent Cloud Setup:**
    a. If you haven't already, sign up for [Confluent Cloud](https://www.confluent.io/confluent-cloud/).
    b. Configure your Kafka producers using the provided sample:
    ```python
    config = {
        'bootstrap.servers': 'YOUR_BOOTSTRAP_SERVER',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': 'YOUR_USERNAME',
        'sasl.password': 'YOUR_PASSWORD'
    }
    ```

2. **Producer Implementation:**
    a. Create an asynchronous producer. You may design your own or reuse the example provided in the class.
    b. Similarly, develop a synchronous producer.

3. **Performance Benchmarking:**
    a. For the testing phase, set `num_messages = 20,000` or larger number.
    b. For both types of producers, track the time taken to send batches of 500 messages. The `time` module in Python will be useful for this task.
    c. Store the elapsed time for each batch in a suitable data structure of your choice.

4. **Analysis:**
    a. Visualize the elapsed time data using a graph (possible tools: `matplotlib` or `seaborn`). The graph should provide insights into the performance variation of the two producers over each batch.
    b. Write an analysis (minimum 150 words) elucidating:
        - The faster producer among the two.
        - Possible reasons for the observed performance differences.
        - Advantages and disadvantages of each producer type.

5. **Deliverables:**
    a. **An organized Python Notebook** (`.ipynb`) encapsulating all your code, visualizations, and concise written analysis.
    b. Ensure your code is **well-commented**, adhering to best practices, and is easy for coworkers to follow.

**Grading Breakdown:**

- Code quality and readability: 3pts
- Data visualization and performance analysis: 2pts
- Extra credit  when you're using your own data schema with dataclass (+1pt) and seriealization (+1pt).

**Notes:** 
- Always back up your code and results.
- Stop the Confluent Cluster if you're not using it. (Save $$)
- Collaboration is encouraged, but direct copying is not. Always cite your sources and collaborators.

--- 

**Problem 2: Reading and Understanding the Kafka Producer**

**Objective:**  
Review and understand the provided [Kafka producer code](https://developer.confluent.io/get-started/python/#build-producer) from the Confluent Developer website. Once you've gone through the code, answer the following questions. Please provide concise and straight forward answers (1-2 sentences.) Understanding the code from other people is important at work. So this exercise will help you hone your skills in reviewing code.

1. **Configuration: 1 pt**
    - What is the purpose of the `config_file` argument in the script?
    - How does the script handle the configuration file to setup the Kafka producer? Mention the Python modules used.
    - Explain the significance of the line `config = dict(config_parser['default'])`.

2. **Producer Instance: 1 pt**
    - How is the Kafka producer instance created in the code?
    - What configuration does it use to set up the producer?

3. **Delivery Callback: 1 pt**
    - What is the purpose of the `delivery_callback` function?
    - In what scenarios is the error message printed in the delivery callback?
    - How is the successful delivery of a message indicated in the callback?

4. **Message Production: 1pt**
    - To which topic are the messages being produced?
    - Describe the logic behind the selection of `user_id` and `product` for each message.
    - What does the `callback` argument do in the `producer.produce()` method?

5. **Final Actions: 1pt**
    - What is the purpose of the `producer.poll(10000)` line? What does the argument `10000` represent?
    - Why is the `producer.flush()` method used *at the end* of the script?

6. **General Understanding: extra credit +1pt**
    - If you were to enhance this script to improve error handling or extend its functionality, what would you recommend?

**Deliverables:**

Please submit your solutions in a file named "assignment1_{your name}". This can be in raw markdown (.md) or text (.txt) format. Ensure your document does not have excessive formatting, as this may distract from the content of your answers.