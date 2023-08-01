FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /donation

# Set the working directory to /music_service
WORKDIR /donation

# Copy the current directory contents into the container at /music_service
ADD . /donation/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
