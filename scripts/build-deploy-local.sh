#! /usr/bin/env sh

# Exit in case of error
set -e

docker-compose down -v --remove-orphans

TAG=latest \
FRONTEND_ENV=${FRONTEND_ENV-production} \
sh ./scripts/build.sh

docker-compose up -d

# You can check the service logs by issuing:
#   >> docker-compose logs
#
# Cleanup when done by issuing:
#   >> docker-compose down --remove-orphans

