# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install curl
RUN apt-get update && apt-get install -y curl

# Set the working directory in the container
WORKDIR /app

# Labels for image metadata
LABEL maintainer="Anes AMRI <anes.devops.31@gmail.com>" \
    name="Docker Monitor App" \
    description="This project monitors new Docker containers and automatically creates proxy hosts on Nginx Proxy Manager using the container's information." \
    version="1.0.0"

# Copy the requirements file into the container
COPY src/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY src/ .

# Command to run the script
CMD ["python", "app.py"]
