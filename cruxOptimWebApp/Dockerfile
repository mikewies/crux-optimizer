FROM python:3
MAINTAINER nanditu@gmail.com
ENV PYTHONUNBUFFERED 1
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD build_development_environment.sh /code/
RUN pip install -r requirements.txt
RUN ./build_development_environment.sh