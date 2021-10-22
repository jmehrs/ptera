#!/bin/bash

# if any command fails, exit as a failure
set -o errexit
# if any variables are not set, exit as a failure
set -o nounset

celery --app app.worker  \
       --broker="${CELERY_BROKER_URL}" \
       beat -S ${CELERYBEAT_SCHEDULER}