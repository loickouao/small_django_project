FROM python:3.8.2
RUN pip install --upgrade pip
RUN pip install pipenv
# Setting PYTHONUNBUFFERED=TRUE allows for log messages to be immediately dumped to the stream instead of being buffered. This is useful for receiving timely log messages
ENV PYTHONUNBUFFERED 1 
RUN mkdir /app
COPY Pipfile* /app/
WORKDIR /app
RUN pipenv lock --requirements > requirements.txt
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

