# Airflow Demo 1: Installing Airflow Locally

This guide provides steps to install Apache Airflow 2.7.3 (the latest version as of now) on your local MacBook. Ensure you follow each step carefully for a successful installation.


### Prerequisites
Before beginning the installation, ensure you have the following prerequisites:

- **Visual Studio Code (VSCode)**
- **Python:** Version 3.10.x is recommended.
- **SQLite Extension for VSCode:** This extension allows for easier management and querying of SQLite databases, a common default database for Airflow in a development environment.


## Step 1: Set Up a Python Virtual Environment

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv 
source .venv/bin/activate  
pip install --upgrade pip
```

## Step 2: Install Apache Airflow 2.7.3

### Set Airflow Home Directory

First, set the `AIRFLOW_HOME` environment variable to specify the Airflow home directory:

```bash
export AIRFLOW_HOME=<path_to_your_airflow_directory>
```

**Note**: To permanently set this variable, add it to your `.bashrc` or `.zshrc` file:

```bash
echo "export AIRFLOW_HOME=<path_to_your_airflow_directory>" >> ~/.zshrc
```

Replace `<path_to_your_airflow_directory>` with the actual path where you want Airflow to store its data.

### Install Airflow via pip

Run the following commands to install the specific version of Airflow:

```bash
AIRFLOW_VERSION=2.7.3
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

## Step 3: Run Airflow - start webserver and scheduler

Start Airflow in standalone mode:

```bash
airflow standalone
```

If you want to run the individual parts of Airflow manually rather than using the all-in-one `standalone` command, you can instead run:

```
airflow db migrate

airflow users create \
    --username admin \
    --firstname airflow \
    --lastname airflow  \
    --role Admin \
    --email wgu9@usfca.edu

airflow webserver --port 8080

airflow scheduler

```
## Step 4: Access Airflow Web UI

Visit `localhost:8080` in your browser. Log in with the admin account (details are shown in the terminal).

Username: admin
Password: (Find it at `<path_to_your_airflow_directory>/standalone_admin_password.txt`)

Enable the `example_bash_operator` DAG on the home page.

## Step 5: Shutting Down Airflow Webserver and Scheduler

To stop Airflow’s webserver and scheduler:

- Identify the process IDs (PIDs) using `ps aux | grep airflow`.
- Use `kill [PID]` to stop the processes.

If you started Airflow in standalone mode with `--deamon`, you can shut it down by terminating the parent process.

The command lsof -i tcp:8080 is used in Unix-like operating systems to list all the processes that are using the TCP port `8080`.

## Additional Resources

For more detailed instructions and troubleshooting, refer to the [official Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/start.html).


## Turn Off the Default Examples in Airflow

By default, Apache Airflow comes with several example DAGs. While these are useful for learning and exploring features, you might want to disable them in a production environment. Here's how to turn off these default examples:

### Edit the Airflow Configuration File

1. **Locate the `airflow.cfg` File**: This file contains the configuration settings for Airflow. It is usually located in the Airflow home directory you set earlier (`$AIRFLOW_HOME`).

2. **Modify the Configuration**: Open the `airflow.cfg` file in a text editor. Look for the line that says `load_examples = True`.

3. **Disable the Examples**: Change this line to `load_examples = False`. This action prevents Airflow from loading the example DAGs when it starts.

### Apply the Changes

After saving the changes to `airflow.cfg`, you need to reset the Airflow database for the changes to take effect:

```bash
airflow db reset
```

**Warning**: The `db reset` command will delete all the data in your Airflow database, including DAGs, logs, and job history. Use this command with caution, especially in a production environment.

### Recreate User Account

Since resetting the database will also remove existing user accounts, you will need to recreate any user accounts you previously had. For example:

```bash
airflow users create \
    --username admin \
    --firstname airflow \
    --lastname airflow \
    --role Admin \
    --email wgu9@usfca.edu
```

Replace the email and username with appropriate values. This command creates a new admin user for Airflow.



