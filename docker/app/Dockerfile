FROM python:3.9.12-buster

ENV GROUP_ID=1000 \
    USER_ID=1000

RUN mkdir -p /var/www/
WORKDIR /var/www/

# Install all build dependencies
RUN apt-get update \
    && apt-get install gcc
RUN pip install --upgrade pip

# install requirements
# cleanup
COPY backend/requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt

COPY backend/app/ /var/www/app/
COPY backend/wsgi.py /var/www/wsgi.py
COPY backend/run.py /var/www/run.py

RUN pip install gunicorn

EXPOSE 5000
RUN ["chmod", "777", "/var/www/"]
