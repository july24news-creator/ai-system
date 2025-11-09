# GitHub Release Instructions for Noakhali AI System

This document provides a template and instructions for creating a new release for the Noakhali AI System on GitHub.

---

## Release Title: `v0.6.0 - Dockerization`

## Release Description

This release introduces Docker support, making it easier than ever to install and run the Noakhali AI System. With a single command, you can start the application without needing to manually install Python or any dependencies.

### Key Features in this Release:

-   **Docker Support:** The entire application is now containerized, providing a consistent and isolated environment.
-   **Simplified Installation:** A `Dockerfile` is included, allowing you to build and run the application with just a few simple Docker commands.
-   **Improved Documentation:** The `README.md` and `INSTALL.md` have been updated with clear instructions for using Docker.

---

## Instructions for Creating the Release

### 1. Build and Push the Docker Image

First, you need to build the Docker image and push it to a container registry, like Docker Hub.

**1. Build the image:**

```bash
docker build -t your-dockerhub-username/noakhali-ai-system:v0.6.0 -f ruinnakbe/Dockerfile .
```

(Replace `your-dockerhub-username` with your actual Docker Hub username)

**2. Log in to Docker Hub:**

```bash
docker login
```

**3. Push the image:**

```bash
docker push your-dockerhub-username/noakhali-ai-system:v0.6.0
```

### 2. Create the Release on GitHub

1.  Go to the **Releases** page of your GitHub repository.
2.  Click **Draft a new release**.
3.  For the **Tag version**, enter `v0.6.0`.
4.  For the **Release title**, enter `v0.6.0 - Dockerization`.
5.  Copy and paste the release description from the top of this file into the **Describe this release** section.
6.  Click **Publish release**.

### 3. Using the Release

Once the release is published, users can pull the Docker image and run the application with the following commands:

**1. Pull the image:**

```bash
docker pull your-dockerhub-username/noakhali-ai-system:v0.6.0
```

**2. Run the application:**

```bash
docker run -p 8080:8080 -v $(pwd)/ruinnakbe/uploads:/app/uploads -v $(pwd)/ruinnakbe/client_secret.json:/app/client_secret.json your-dockerhub-username/noakhali-ai-system:v0.6.0
```

The application will then be available at [http://localhost:8080](http://localhost:8080).
