FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -qq -y \
    build-essential libpq-dev postgresql-client \
    gdal-bin postgis libgdal-dev --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .
