FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install --assume-yes \
        python3.10 python3-pip \
        pkg-config fonts-liberation xdg-utils \
        software-properties-common curl unzip wget \
        xvfb firefox firefox-geckodriver && \
    apt-get clean all

RUN apt-get update && apt-get install --assume-yes libpq-dev gcc && apt-get clean all

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

