FROM python:3.8.3-slim-buster

# set work directory


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/sibdev
# install dependencies

COPY ./requirements.txt /user/src/requirements.txt

RUN pip install -r /user/src/requirements.txt

# copy project
COPY . /user/src/sibdev

EXPOSE 8000
#
CMD python /user/src/sibdev/manage.py migrate --noinput && python /user/src/sibdev/manage.py runserver 0.0.0.0:8000