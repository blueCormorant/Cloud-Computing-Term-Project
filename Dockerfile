# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory in the container to /app
WORKDIR /app

# Add current directory code to /app in the container
ADD . /app

# Update the environment with any environment.yml dependencies
RUN conda env create -f environment.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "ScienceGateway", "/bin/bash", "-c"]

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make ports available to the world outside this container
EXPOSE 8000 6379
