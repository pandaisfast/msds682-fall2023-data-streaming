# ReadMe

## Virtual Environment Setup

A virtual environment is a tool that helps to keep dependencies required by different projects separate. It essentially allows you to create a virtual Python environment that is isolated from the global Python environment. This way, different projects can have different dependencies without any conflicts.

### Setting up a Virtual Environment

1. **Create a Virtual Environment**:
   Navigate to your project directory in the terminal and run the following command to create a new virtual environment named `venv`:
   
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:

   - **Linux & Mac**:
     
     ```bash
     source venv/bin/activate
     ```

   - **Windows (PowerShell)**:

     ```bash
     .\venv\Scripts\Activate.ps1
     ```

3. **Install Required Packages**:

   After activating your virtual environment, you can install required packages using pip. If the project provides a `requirements.txt` file, you can install all the required packages with:

   ```bash
   pip install -r requirements.txt
   ```

   This command will install the versions of packages as mentioned in `requirements.txt`.

---

## Specifying Python Kernel within Jupyter Notebook (ipynb)

If you're using Jupyter Notebook or Jupyter Lab, it's important to ensure that the notebook is using the correct Python kernel, especially if you have multiple Python environments or versions.

1. **Install `ipykernel`**:
   
   After activating your virtual environment, ensure you have `ipykernel` installed:

   ```bash
   pip install ipykernel
   ```

2. **Choose the Correct Kernel in Jupyter**:

   - Start Jupyter Notebook or Jupyter Lab.
   - Open your `.ipynb` notebook.
   - From the menu, go to `Kernel` -> `Change kernel` and select `venv` (or the name you provided in the previous step).
   
Now, your Jupyter notebook will use the Python version from your virtual environment and any packages you've installed in it.