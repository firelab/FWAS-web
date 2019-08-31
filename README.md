# Fire Weather Alert Service

## Overview


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
