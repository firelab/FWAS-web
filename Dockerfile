##############################################################################
# Step 1: Build all dependencies into .whl files
# 
# Dependencies will be removed in the second stage to reduce the total 
# image size
##############################################################################
FROM python:3.7-alpine as build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD requirements.txt /app/
WORKDIR /app

RUN apk update && \
    apk add --no-cache --virtual build-deps \
        make gcc \
        python3-dev musl-dev libffi-dev openssl-dev postgresql-dev && \
    python3 -m ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel

# Install all requirements. Leverages docker layer caching to
# speed up the build phase.
RUN pip wheel --wheel-dir=dist -r requirements.txt

# Add the package source and create a wheel. Will be installed
# in the next stage.
ADD . /app
RUN python3 setup.py bdist_wheel


##############################################################################
# Step 2: build the Flask app image
# 
# Uses the wheels created from the first step to reduce the
# build times and remove the need to store the source directory
# in the image.
##############################################################################
FROM ubuntu:bionic

WORKDIR /app

# System dependencies are installed
# prior to the copy because they can take awhile on ubuntu.
RUN set -xe \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update -q && \
    apt-get install -y -q python3.7 python3-pip binutils libproj-dev gdal-bin

COPY --from=build /app/dist/*.whl dist/
COPY --from=build /app/bin /app/bin
COPY --from=build /app/config /app/config/

RUN set -xe \
    python3.7 -m pip install --no-cache --upgrade pip setuptools wheel&& \
    python3.7 -m pip wheel --wheel-dir=dist psycopg2-binary && \
    python3.7 -m pip install --find-links . --no-index dist/*.whl && \
    apt-get remove -y python3-pip python3-wheel && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -r dist && \
    rm -rf /var/lib/apt/lists/* && \
    useradd appuser --no-create-home --user-group && \
    chmod 777 /run/ -R && \
    chmod 777 /root/ -R 


USER appuser

EXPOSE 5000
