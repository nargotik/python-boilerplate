#!/bin/sh

export APP_VERSION=$(cat /VERSION)

exec "$@"
