FROM ubuntu:16.04
WORKDIR /opt/app/server
COPY requirements.txt /opt/app/server/requirements.txt
ADD . /opt/app/server

ARG APP_HOST=0.0.0.0
ENV APP_HOST="${APP_HOST}"

ARG APP_PORT=8080
ENV APP_PORT="${APP_PORT}"

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/server/static


FROM python:3.6.5
COPY . /opt/app/server
RUN pip3 install -r /opt/app/server/requirements.txt
