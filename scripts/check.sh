#!/usr/bin/env bash

set -eux

cd $(dirname $0)/..

poetry run flake8 mbdata_graphql
poetry run mypy mbdata_graphql
poetry run pytest mbdata_graphql
