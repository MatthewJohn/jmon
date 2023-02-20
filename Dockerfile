FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install --assume-yes \
        python3.10 python3-pip \
        pkg-config fonts-liberation xdg-utils \
        software-properties-common curl unzip wget \
        xvfb firefox firefox-geckodriver \
        chromium-browser && \
    apt-get clean all

RUN wget https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin

RUN apt-get update && apt-get install --assume-yes libpq-dev gcc && apt-get clean all

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

