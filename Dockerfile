FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD . /app

COPY ./requirments.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
