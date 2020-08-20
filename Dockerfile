# Base Image
FROM ubuntu:18.04 as base

# Set a working directory
WORKDIR /usr/src/

# Set default environment variables
ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Set environment variables
ENV DJANGO_SETTINGS_MODULE kaliblog.settings.prod
ENV AWS_ACCESS_KEY_ID AKIAJBIKJM76JCK3YQ6A
ENV AWS_SECRET_ACCESS_KEY 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

# Install Ubuntu dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    libopencv-dev \
    build-essential \
    libssl-dev \
    libpq-dev \
    libcurl4-gnutls-dev \
    libexpat1-dev \
    gettext \
    unzip \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

# Install environment dependencies
RUN pip3 install --upgrade pip
RUN pip3 install psycopg2

# Install project dependencies
COPY ./requirements.txt /usr/src
RUN pip3 install -r requirements.txt

# Copy project to working directory
COPY . /usr/src


# RUN server
CMD gunicorn kaliblog.wsgi:application --bind 0.0.0.0:$PORT