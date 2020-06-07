FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
#pipenv lock --requirements > requirements.txt
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
