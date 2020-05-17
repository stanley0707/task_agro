FROM ubuntu:16.04
WORKDIR /opt/app/server
COPY requirements.txt /opt/app/server/requirements.txt
ADD . /opt/app/server

# ENV STATIC_URL /static
# ENV STATIC_PATH /var/www/app/server/static

FROM python:3.7
COPY . /opt/app/server
COPY manage.py /opt/app/server/manage.py

RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/app/server/requirements.txt

