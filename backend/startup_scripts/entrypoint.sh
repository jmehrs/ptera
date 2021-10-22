#!/bin/bash

# if any command fails, exit as a failure
set -o errexit
# if any pipe commands fail, exit as a failure
set -o pipefail
# if any variables are not set, exit as a failure
set -o nounset

broker_ready() {
python << END
import sys
from kombu.connection import Connection
from kombu.exceptions import OperationalError

max_retries=5
interval_step=5
interval_max=10

try:
    with Connection('${CELERY_BROKER_URL}') as conn:
        conn.ensure_connection(
            max_retries=max_retries,
            interval_step=interval_step, 
            interval_max=interval_max, 
            callback=lambda: print('Waiting for broker to become available...')
        )
except OperationalError as err:
    print(
        f'Could not establish a connection with the broker, exiting: {err}',
        file=sys.stderr
    )
    sys.exit(-1)

print('Broker is now available')
sys.exit(0)
END
}

broker_ready

exec "$@"