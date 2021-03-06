# Dockerfile

# Pull base image
FROM python:3.8.2
# Set environment variables
# Setting PYTHONUNBUFFERED=TRUE allows for log messages to be immediately dumped to the stream instead of being buffered. This is useful for receiving timely log messages
# PYTHONDONTWRITEBYTECODE means Python wont try to write .pyc files which we also do not desire
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1
# Set work directory
RUN mkdir /app
WORKDIR /app
# Install dependencies
COPY Pipfile* /app/
RUN pip install --upgrade pip
RUN pip install pipenv
#RUN pipenv install --dev --system --deploy --ignore-pipfile
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

# Copy project
COPY . /app/
