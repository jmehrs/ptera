#!/bin/bash

# if any command fails, exit as a failure
set -o errexit
# if any variables are not set, exit as a failure
set -o nounset

worker_ready() {
    celery -A app.worker inspect ping
}


until worker_ready; do
  >&2 echo 'Waiting for worker to become available...'
  sleep 1
done
>&2 echo 'Worker is available'

celery --app app.worker  \
       --broker="${CELERY_BROKER_URL}" \
       flower