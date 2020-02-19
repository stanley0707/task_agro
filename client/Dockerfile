FROM ubuntu:16.04
WORKDIR /opt/app/client
COPY requirements.txt /opt/app/server/requirements.txt
ADD . /opt/app/client

ARG APP_HOST=0.0.0.0
ENV APP_HOST="${APP_HOST}"

ARG APP_PORT=8080
ENV APP_PORT="${APP_PORT}"

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/client/static


FROM python:3.6.5
COPY . /opt/app/client
RUN pip3 install -r /opt/app/client/requirements.txt
