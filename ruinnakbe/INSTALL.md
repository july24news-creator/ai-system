# How to Install and Run Noakhali AI System

This document provides instructions on how to install and run the Noakhali AI System web application.

## Prerequisites

- Python 3 (https://www.python.org/downloads/)
- `pip` (usually comes with Python)

## 1. Get the Code

First, get the application code. You can do this by cloning the repository:

```bash
git clone <repository-url>
cd ruinnakbe
```

## 2. Install Dependencies

This project uses the Flask web framework and the Google Drive API. You can install all the necessary dependencies using the `requirements.txt` file:

```bash
pip3 install -r requirements.txt
```

## 3. Set up Google Drive Credentials (Optional)

If you want to use the Google Drive integration, you will need to get API credentials from the Google Cloud Console.

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project.
3.  Search for and enable the **Google Drive API**.
4.  Go to the **Credentials** page.
5.  Click **Create Credentials** and select **OAuth client ID**.
6.  Choose **Desktop app** as the application type.
7.  Click **Download JSON** to download your credentials file.
8.  Rename the downloaded file to `client_secret.json` and place it in the `ruinnakbe` directory.
9.  You can use the `client_secret.json.example` file as a template to make sure you have the correct format.

## 4. Run the Web Application

To start the application, run the `main.py` script:

```bash
python3 main.py
```

This will start a local web server.

## 5. View the Application

Open your favorite web browser and go to the following address:

[http://127.0.0.1:8080](http://127.0.0.1:8080)
