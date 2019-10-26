# Fire Weather Alert Service

## Overview

System for defining alerts based on location and weather data to notify fire response personnel of threatening weather situations. Alerts are specific to the individual and are created on the client interface. Alerts are stored on a server and compared with weather data to generate notifications.

## Installation

First, install `fwas` 
into the `pipenv` environment.  This will allow you
to use the CLI for the app.
```
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
fwas run
fwas routes
fwas db migrate
```

### API

## Design

![fwas_design](docs/fwas_design.png)

### TODO

- [ ] use ansible for production deploys (over Docker Swarm to minimize operational complexity)
- [ ] add in token-based (JWT) authentication to the API
