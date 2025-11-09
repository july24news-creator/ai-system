# Noakhali AI System

A simple web application with a command interface, file uploading, file listing, and Google Drive integration.

## Features

- **Google Drive Integration:** Connect to your Google Drive account to view your files.
- **Command Interface:** Execute simple text-based commands.
- **File Upload:** Upload files to the server.
- **File Listing:** View a list of all uploaded files.
- **Timestamp Display:** Shows the current server timestamp.

## How to run

1.  Clone the repository.
2.  Install the dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

3.  **Set up Google Drive Credentials:**
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project.
    - Enable the Google Drive API.
    - Create an OAuth 2.0 Client ID for a "Desktop app".
    - Download the JSON credentials file.
    - Rename the downloaded file to `client_secret.json` and place it in the `ruinnakbe` directory.
    - **Important:** Make sure your `client_secret.json` file contains your actual credentials. You can use the `client_secret.json.example` as a template.

4.  Run the application with the following command:

    ```bash
    python3 main.py
    ```

5.  Open your web browser and navigate to `http://127.0.0.1:8080` to see the application.
