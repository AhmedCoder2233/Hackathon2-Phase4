# Quickstart: Backend Docker Image

This guide explains how to build and run the backend service using the provided `Dockerfile`.

## Prerequisites

*   Docker must be installed and running on your system.

## Building the Image

1.  Navigate to the root directory of the project in your terminal.
2.  Run the following command to build the Docker image:

    ```bash
    docker build -t chatbot-backend:latest -f backend/Dockerfile .
    ```

    *   `-t chatbot-backend:latest` tags the image with the name `chatbot-backend` and tag `latest`.
    *   `-f backend/Dockerfile` specifies the location of the `Dockerfile`.
    *   `.` sets the build context to the root of the project, allowing the `Dockerfile` to access files from the entire project.

## Running the Container

1.  Once the image is built, you can run it as a container with this command:

    ```bash
    docker run -d -p 8000:8000 --name chatbot-backend-container chatbot-backend:latest
    ```

    *   `-d` runs the container in detached mode (in the background).
    *   `-p 8000:8000` maps port 8000 on your host machine to port 8000 in the container, where the application is running.
    *   `--name chatbot-backend-container` gives the running container a memorable name.

2.  The backend service should now be running and accessible at `http://localhost:8000`.
