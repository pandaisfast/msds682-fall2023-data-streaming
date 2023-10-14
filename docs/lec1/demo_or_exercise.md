# Demo #1 Setting Up Environment

## Principles in our demos

- **You should focus more on learning the core concepts and applications than setting up environment.** Environment setup and cluster management are usually not the responsibility of new hires, especially in large companies with dedicated ops teams. 
- **Don't spend too much time on complex cluster configuration and environment setup as a beginner.** This can detract you from learning the fundamentals. Focus more on the higher level abstractions and use cases.
- **Leverage existing documentation and sample code.** Don’t reinvent the wheel.
- **Take an iterative approach to learning.** Get the basics working first, and later dive into refinement, optimizations and customizations. 

--- 
We have two options of setting up Kafka clusters here. The first one with Confluent Cloud + CLI (python) will be used in our classroom. 

### Method #1: Confluent Cloud + CLI

#### Overview
Confluent Cloud is a managed Kafka service provided by Confluent, the company behind some of the popular Kafka toolsets. The significant advantage of using Confluent Cloud is that you don't have to worry about the infrastructure or configuration of a Kafka cluster. Everything is managed, and you can focus entirely on your application and client development. This method is used in the classroom.

#### Benefits
1. **Simplicity**: No need to set up or maintain the Kafka cluster.
2. **Scalability**: Managed services often offer easy ways to scale your usage as needed.
3. **Reliability**: Managed by experts, ensuring high availability, backups, and other best practices.

### Method #2: Local Cluster (self-managed)

#### Overview
This is about setting up a Kafka cluster on your local machine, often for development or testing purposes. There are resources available in the official documentation to guide through this setup. 

#### Docker with Confluent Platform
Docker provides a way to run applications securely isolated in a container, packaged with all its dependencies and libraries. The links you provided are guides on setting up the Confluent Platform (which includes Kafka and other tools) using Docker containers.

**Note**: the native Kafka installation is another option, though Docker provides isolation benefits.

1. **Confluent Platform Quickstart with Docker**: This provides a quick way to get up and running with the entire Confluent Platform on your local machine using Docker. The platform includes Kafka, Confluent Schema Registry, Kafka Connect, and more. The quickstart guide will walk you through the basics of setting it up.

2. **Docker Installation for Confluent Platform**: This is a more detailed guide on installing and using the Confluent Platform with Docker. It covers prerequisites, installation steps, and other important information.

#### Benefits of Docker-based Local Setup
1. **Isolation**: Ensures Kafka doesn't interfere with other software on your machine.
2. **Reproducibility**: A consistent setup across different machines.
3. **Ease of Setup & Cleanup**: With a few commands, you can start and stop a Kafka cluster.

## Instructions (Method #1)

**Step 1.Confluent Cloud Account**: Sign up and be aware of the $400 free credit. [Link](https://www.confluent.io/confluent-cloud/tryfree/?session_ref=https://developer.confluent.io/courses/kafka-python/intro/&_gl=1*1e4ufod*_ga*MTg5NDI2ODI5Ny4xNjk1NTEwNjc0*_ga_D2D3EGKSGD*MTY5NzMwNzI2Ni4yNC4xLjE2OTczMDczNDYuNTIuMC4w&_ga=2.204271120.1862646819.1697302973-1894268297.1695510674&_gac=1.188677466.1695601991.Cj0KCQjwvL-oBhCxARIsAHkOiu0Qq0KqM4-LH4cC6o3wgdTVyQEfSfrYdVRJYwbdU1dcwF4afsnO1kgaAsvqEALw_wcB).


<div class="result" markdown>

![Web_2](<../assets/demo_or_exercise/demo1 - 1.png>){align=left width=600}
<div style="clear:both;"></div>
</div>


---

**Step 2. Creating & Running Confluent Cluster**: Set up a Kafka cluster on Confluent Cloud.

**Create Cluster**

<div class="result" markdown>

![Web_3](<../assets/demo_or_exercise/demo1 - 2.png>){align=left width=600}
<div style="clear:both;"></div>
</div>

<div class="result" markdown>

![Web_4](<../assets/demo_or_exercise/demo1 - 3.png>){align=left width=600}
<div style="clear:both;"></div>
</div>

<div class="result" markdown>

![Web_2](<../assets/demo_or_exercise/demo1 - 4.png>){align=left width=600}
<div style="clear:both;"></div>
</div>

---

**Create Topic**
Let's create topic called "demo1_free_text". Produce 8 messages with same `key = 1` and different `sport` values. 

```
value: {
      "sport": "400 metres"
}

key: 1
```

<div class="result" markdown>

![Web_2](<../assets/demo_or_exercise/demo1 - 5.png>){align=left width=600}
<div style="clear:both;"></div>
</div>


<div class="result" markdown>

![Web_2](<../assets/demo_or_exercise/demo1 - 6.png>){align=left width=600}
<div style="clear:both;"></div>
</div>



<div class="result" markdown>

![Web_2](<../assets/demo_or_exercise/demo1 - 7.png>){align=left width=600}
<div style="clear:both;"></div>
</div>


<div class="result" markdown>

![Web_2](<../assets/demo_or_exercise/demo1 - 8.png>){align=left width=600}
<div style="clear:both;"></div>
</div>


--- 

Do **NOT** shutdown the cluster. Let's go to the next section to set up CLI. We will come back to this Confluent UI later in the end of the instructions.

**Step 3. Python 3**: Make sure it's version `3.10.12` for consistency. If you already have python 3.10.x set up, then you can skip Step 3.

**3.1 Environment**

- Use a Macbook with Ventura 13.5.x. *Avoid upgrading to MacOS 14.0 Sonoma*.
- Ensure `pip` (Python's package manager) is up-to-date.
- Install `brew` if you haven't. It's a handy tool for Mac users. Please run `brew install brew` to update it to latest version.

- Consider using a Python virtual environment. It helps keep things tidy!
- Before the demo, check your setups. For instance, verify the Python version with `python --version`.
- If you face setup issues, don't worry! We'll ensure everyone can follow along.

**3.2 Installing ASDF**

To manage python packages, ASDF can be installed on macOS using Homebrew:

```bash
brew install asdf
```

After installation, ensure ASDF is added to your shell.

For zsh:


```bash
echo -e "\n. $(brew --prefix asdf)/libexec/asdf.sh" >> ${ZDOTDIR:-~}/.zshrc
```

For bash:


```bash
echo -e "\n. $(brew --prefix asdf)/libexec/asdf.sh" >> ~/.bash_profile
```

**3.3 Using ASDF**


Here are some commonly used ASDF commands:

List all available plugins:

bash

```bash
asdf plugin list all | grep -i <plugin>
```

List installed plugins:

bash

```bash
asdf plugin list
```

Add plugins:

bash

```bash
asdf plugin add python 
asdf plugin add poetry
```

Install specific versions:

bash

```bash
asdf install python 3.10.12
# asdf uninstall python 3.10.8

asdf list-all python
```

**3.4 Error**
```
ModuleNotFoundError: No module named '_lzma'
WARNING: The Python lzma extension was not compiled. Missing the lzma lib?
```
-> simply install it via ```brew install xz```

Great, you have successfully installed `Python 3.10.12` with asdf. Here's what you might want to do next:

**3.5 Set the Python version**

Now that you have Python 3.10.12 installed, you might want to set it as your default version. You can do this with asdf's global command:

```bash
asdf global python 3.10.12
```
This will make Python 3.10.12 your default Python version in all directories.

Alternatively, if you want to use this Python version only in your current directory (for a specific project), you can use asdf's local command:

```bash
asdf local python 3.10.12
```

**Step 4. Installing Confluent CLI**

Install the Confluent CLI and follow [this official guide](https://docs.confluent.io/confluent-cli/current/install.html). 


You can update it to latest CLI version by running `brew upgrade confluentinc/tap/cli` (assuming you installed CLI via `brew`).

My version of Confluent CLI: `3.38.0`.

**Step 5. Setting up Confluent CLI**

Again, I recommend using [official guide](https://docs.confluent.io/confluent-cli/current/overview.html) for most up-to-date information. In our demo today, here are the key steps below.

**Environment**: In Confluent Cloud, an environment is a logical workspace where you can organize your resources. You can think of it like a project folder in many other systems. One user can have multiple environments.

**Cluster**: Within an environment, you can have one or more Kafka clusters. A cluster is essentially a running instance of Kafka, where you can produce and consume messages. 

1. **Logging in to Confluent Cloud**: 
    ```bash
    confluent login --save
    ```
    This logs you into Confluent Cloud via the CLI and saves your credentials locally, so you don't need to enter them repeatedly.

2. **Listing Environments**:
    ```bash
    confluent environment list
    ```
    This lists all the environments you have access to. For a new account, this will typically be just one environment. Make note of the ID of the environment you want to use.

3. **Setting the Active Environment**:
    ```bash
    confluent environment use {ID}
    ```
    With this command, you're telling the CLI: "Hey, I want to work within this specific environment."

4. **Listing Clusters**:
    ```bash
    confluent kafka cluster list
    ```
    This lists all the Kafka clusters within the currently active environment. Make note of the cluster ID you want to interact with.

5. **Setting the Active Cluster**:
    ```bash
    confluent kafka cluster use {ID}
    ```
    This command sets the Kafka cluster you want to work with. All subsequent commands will interact with this cluster unless you change it.

6. **Creating an API Key**:
    ```bash
    confluent api-key create --resource {ID}
    ```
    An API key and secret are needed to authenticate and interact with your Kafka cluster programmatically. The `--resource {ID}` is the cluster ID you've previously noted. This command will provide you an API key and secret. Keep them safe; you'll need them to authenticate your requests.

7. **Using the API Key**:
    ```bash
    confluent api-key use {API Key} --resource {ID}
    ```
    This tells the CLI to use the provided API key for authentication when interacting with the specified resource (Kafka cluster).

---


**Step 6. Managing topics with Confluent CLI**

In this step, we'll learn how to manage Kafka topics using the Confluent CLI. We'll produce some messages to a topic and consume them to see how Kafka handles message streams.

**6.1 Listing Existing Topics**:
Before diving into producing and consuming messages, let's see which topics are already available in your Kafka cluster:

```bash
confluent kafka topic list
```

**6.2 Producing and Consuming Messages**:
To truly understand Kafka, it's beneficial to visualize the interaction between a producer (which sends messages) and a consumer (which reads messages). For this, we'll open two terminal windows: one for the producer and one for the consumer.

* **Terminal 1: Producer's Perspective**:

      To send messages to a topic, use the following command:
      
      ```bash
      confluent kafka topic produce {topic_name} --parse-key
      ```
      
      Now, input the following messages:
      
      ```
      1:"200 metres"
      1:"100 metres"
      1:"archery"
      ```

* **Terminal 2: Consumer's Perspective**:

      To read messages from a topic, use the following command:
      
      ```bash
      confluent kafka topic consume --from-beginning {topic_name}
      ```

      Observe the messages appearing in real-time as they’re produced in Terminal 1.

**6.3 Verifying in Confluent Cloud UI**:

After producing and consuming messages using the CLI, it's a good practice to check the Confluent Cloud UI to see the data visually:

- Go to Confluent Cloud.
- Navigate to the topic overview page for the topic you chose.
- Click on the **Messages** tab.
- In the **Jump to offset** field, enter "0".
- Select different partitions to observe where the new messages have been stored.

---

## Summary

There are many concepts so far. I hope to give a clear picture of the relationship between the different components of Confluent Cloud and how they are accessed via the CLI. Let's break down the hierarchy and relationship of the Confluent Cloud UI and how it interacts with the CLI.

### Confluent Cloud Hierarchy:

1. **Environment**:
   - An environment is the highest level of organization in Confluent Cloud. It's a logical grouping mechanism.
   - You might have different environments for different purposes, such as Development, Testing, and Production.
   - Each environment has a unique **Environment ID**.

2. **Cluster**:
   - *Within an environment*, you can have one or more Kafka clusters.
   - Each cluster has its resources, such as brokers, topics, etc.
   - Each cluster has a unique **Cluster ID** within the environment.

### Accessing via CLI:

To access and manage resources within Confluent Cloud using the CLI, you often need to specify both the environment and cluster you want to interact with. This is especially true if you have multiple environments or clusters, as many organizations do.

Typically, the process involves:

1. **Authentication**:
   - You'll first authenticate your CLI with Confluent Cloud using your API key and secret.

2. **Setting the Environment**:
   - Use the Environment ID to specify which environment you want to work within.

3. **Accessing/Managing a Cluster**:
   - Once inside an environment, use the Cluster ID to specify which cluster you want to interact with.

### Example:

Imagine you have two environments: `Development` and `Production`. In the `Development` environment, you have a Kafka cluster named `DevCluster`.

To manage a resource in `DevCluster` using the CLI:

1. Authenticate your CLI with Confluent Cloud.
2. Set your working environment to `Development` using its Environment ID.
3. Access or manage `DevCluster` using its Cluster ID.

### Conceptual Visualization:

```
Confluent Cloud
|
|-- Environment 1 (Development)
|   |
|   |-- Cluster A (DevCluster)
|   |   |
|   |   |-- Topic 1
|   |   |-- Topic 2
|   |
|   |-- Cluster B
|
|-- Environment 2 (Production)
    |
    |-- Cluster C
    |
    |-- Cluster D
```

When working with the Confluent CLI, you'd authenticate, select Environment 1 (using its ID), then select Cluster A (using its ID) to interact with topics or other resources within that cluster.