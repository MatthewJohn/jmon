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

RUN wget "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1072663%2Fchrome-linux.zip?generation=1668668877454764&alt=media" -O chrome-linux.zip && \
    unzip chrome-linux.zip && \
    rm chrome-linux.zip && \
    mv chrome-linux /opt/

RUN wget "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1072663%2Fchromedriver_linux64.zip?generation=1668668883584549&alt=media" -O chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver_linux64/chromedriver /usr/local/bin

RUN apt-get update && apt-get install --assume-yes libpq-dev gcc && apt-get clean all

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

