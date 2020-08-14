# Pull a base image (Python3.8, in this case)
FROM python:3.8

# SET ENVIRONMENT VARIABLES
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# SET WORKING DIRECTORY
WORKDIR /code

# REQUIREMENTS INSTALLATION
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# COPY PROJECT
COPY . /code/