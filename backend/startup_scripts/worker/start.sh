#!/bin/bash

# if any command fails, exit as a failure
set -o errexit
# if any variables are not set, exit as a failure
set -o nounset



mkdir -p /var/run/celery
chown -R nobody:nogroup /var/run/celery

celery --app app.worker worker \
       --loglevel INFO \
       --statedb=/var/run/celery/%p.state \
       --hostname=${PROJECT_NAME}@%h \
       --uid=nobody \
       --gid=nogroup
