FROM python:3.8.2
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
#RUN pipenv lock --requirements > requirements.txt
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

