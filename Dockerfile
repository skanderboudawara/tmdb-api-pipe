# Use the official Python image from the Docker Hub
FROM python:3.10-slim

USER root

# Set the working directory in the container
WORKDIR /app

RUN apt update -y && \
    apt install -y nano

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt


