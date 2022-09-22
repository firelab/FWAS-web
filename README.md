# Web version of the Fire Weather Alert System

## Overview

System for defining alerts based on location and weather data to notify fire response personnel of threatening weather situations. Alerts are specific to the individual and are created on the client interface. Alerts are stored on a server and compared with weather data to generate notifications.

## Installation

First, install `fwas` 
into the `pipenv` environment.  This will allow you
to use the CLI for the app.
```
pipenv install
pipenv run pip install -e .
```


## Usage

### From the command-line
You can then use `fwas` as
the command-line tool. It is a wrapper around `flask`
but creates the application without specifying environment
variables. Any command you can run after `flask` is
available to run as `fwas`.

*Examples*:
```
. /venv/bin/activate
pip install -e .

fwas runworker
rqscheduler
```

Running locally requires PostGIS and Redis. A `docker-compose.yaml` file is 
provided to run those for you. Run `docker-compose up -d` to start both
PostGIS and Redis.

### API

Exposed endpoint documentation is available through (localhost:8000/docs)[http://localhost:8000/docs].

## Design

![fwas_design](docs/fwas_design.png)


