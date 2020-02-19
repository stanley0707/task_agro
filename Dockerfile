FROM ubuntu:16.04
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app

ADD . /opt/app

ARG APP_HOST=0.0.0.0
ENV APP_HOST="${APP_HOST}"

ARG APP_PORT=8080
ENV APP_PORT="${APP_PORT}"

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static


FROM python:3.6.5
COPY . /opt/app
RUN pip3 install -r /opt/app/requirements.txt
