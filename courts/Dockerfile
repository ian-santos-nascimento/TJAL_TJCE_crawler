FROM python:3.9 AS base

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE courts.settings

RUN pip install --upgrade pip && pip install scrapyd

# Create and set the working directory in the container
WORKDIR /code

# Copy only requirements first to leverage Docker caching
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire codebase
COPY . .
