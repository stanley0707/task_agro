FROM ubuntu:16.04
WORKDIR /opt/app/client
COPY requirements.txt /opt/app/server/requirements.txt
ADD . /opt/app/client


# ENV STATIC_URL /static
# ENV STATIC_PATH /var/www/app/client/static

FROM python:3.7
COPY . /opt/app/client
RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/app/client/requirements.txt
