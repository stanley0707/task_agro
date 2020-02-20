FROM ubuntu:16.04
WORKDIR /opt/app/server
COPY requirements.txt /opt/app/server/requirements.txt
ADD . /opt/app/server

ARG APP_HOST=0.0.0.0
ENV APP_HOST="${APP_HOST}"

ARG APP_PORT=8080
ENV APP_PORT="${APP_PORT}"

ARG DEBUG=True
ENV DEBUG="${DEBUG}"

ARG CLIENT_PORT=8081
ENV CLIENT_PORT="${CLIENT_PORT}"

ARG CLIENT_HOST=0.0.0.0
ENV CLIENT_HOST="${CLIENT_HOST}"

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/server/static


FROM python:3.6.5
COPY . /opt/app/server
RUN pip3 install -r /opt/app/server/requirements.txt
