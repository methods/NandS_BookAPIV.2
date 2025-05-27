# NandS_BookAPIV.2

## Project Overview

This project provides a books API that will allow users to add, retrieve, reserve and edit books on a database. 

- [Contributing Guidelines](CONTRIBUTING.md)
- [License Information](LICENSE.md)

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3**: Version 3.7 or newer is recommended. You can download it from [python.org](https://www.python.org/downloads/).
*   **pip**: Python's package installer. It usually comes with Python installations.
*   **venv** (recommended): Python's built-in module for creating virtual environments.

## Setup and Installation

1. **Clone the repository:**
    
    Clone project from the git repository:
    ```bash
    git clone git@github.com:methods/NandS_BookAPIV.2.git
    cd NandS_BookAPIV.2
    ```

2.  **Create a virtual environment (recommended):**
    
    It's good practice to use a virtual environment to manage project dependencies.
    ```bash
    python3 -m venv venv
    ```

    This creates a `venv` folder in your project directory.

3.  **Activate the virtual environment:**

    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows (Command Prompt):
        ```bash
        venv\Scripts\activate.bat
        ```
    *   On Windows (PowerShell):
        ```bash
        .\venv\Scripts\Activate.ps1
        ```
    Your command prompt should now indicate that the virtual environment is active (e.g., `(venv) Your-User@Your-Machine ...$`).

4.  **Install dependencies:**
    
    This project requires Flask - see 'requirements.txt' file for list of dependencies.
    To install dependencies in the `requirements.txt` file, run 
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the API

1.  Ensure your virtual environment is activated (see step 3 in Setup).
2.  Navigate to the project directory where `app.py` is located.
3.  Run the Flask application:

    ```bash
    Flask --debug run
    ```
    You should see output similar to this, indicating the server is running:
    ```
     * Serving Flask app 'app'
     * Debug mode: on
     * WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: xxx-xxx-xxx
    ```

## How to Run Linting
This project uses **Pylint** to check code quality and style.

To run the linter:

1. Open your terminal.
2. Make sure your virtual environment is activated.
3. Ensure the linter script is executable by running:

```bash
chmod +x run_pylint.sh
```

4. Run the following command:

```bash
./run_pylint.sh
```



## How to Run Tests

This project utilizes **Pytest** - in order to run the test
1. On the terminal run:

    ```bash
    pytest test_app.py
    ```

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.