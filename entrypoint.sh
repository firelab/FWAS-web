#!/bin/bash


set -euo pipefail

sleep 10

alembic upgrade head

exec uvicorn fwas.main:app --host=0.0.0.0 --port=8000 --reload
