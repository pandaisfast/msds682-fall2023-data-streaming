# Airflow Demo



# Demo 1A: Installing Airflow Locally

This guide provides steps to install Apache Airflow 2.7.3 (the latest version as of now) on your local MacBook. Ensure you follow each step carefully for a successful installation.

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

## Step 3: Run Airflow

Start Airflow in standalone mode:

```bash
airflow standalone
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

Alternatively, if you started Airflow in standalone mode with `-D`, you can shut it down by terminating the parent process.

## Additional Resources

For more detailed instructions and troubleshooting, refer to the [official Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/start.html).


# Demo 1B: Installing Airflow Locally