FROM python:3
MAINTAINER nanditu@gmail.com
ENV PYTHONUNBUFFERED 1
/usr/local/bin/python -m pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
