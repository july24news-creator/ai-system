# How to Install and Run Noakhali AI System

This document provides instructions on how to install, run, and build the Noakhali AI System web application.

## Prerequisites

- Python 3 (https://www.python.org/downloads/)
- `pip` (usually comes with Python)

## Running the Application from Source

### 1. Get the Code

First, get the application code. You can do this by cloning the repository:

```bash
git clone <repository-url>
cd ruinnakbe
```

### 2. Install Dependencies

This project uses the Flask web framework. You can install it using the `requirements.txt` file:

```bash
pip3 install -r requirements.txt
```

### 3. Run the Web Application

To start the application, run the `main.py` script:

```bash
python3 main.py
```

This will start a local web server.

### 4. View the Application

Open your favorite web browser and go to the following address:

[http://127.0.0.1:8080](http://127.0.0.1:8080)

You should see the Noakhali AI System application running.

## Building a Standalone Executable

You can also build a standalone executable for the application. This will package the application and all its dependencies into a single file.

### 1. Install PyInstaller

You will need to install the `pyinstaller` package to build the executable. You can install it using `pip`:

```bash
pip3 install pyinstaller
```

### 2. Build the Executable

To build the executable, run the following command from the `ruinnakbe` directory:

```bash
pyinstaller --onefile --add-data "templates:templates" main.py
```

This will create a `dist` directory containing the executable file named `main`.

### 3. Run the Executable

You can run the application by executing the file created in the `dist` directory:

```bash
./dist/main
```

This will start the web server, and you can view the application in your browser as described above.
