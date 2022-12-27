#!/usr/bin/env sh

CONTAINER_ID=$(docker ps -aq --filter "name=m3-frontend")

if [ -n "$CONTAINER_ID" ]; then
  echo "### Removing old container..."
  docker rm -f "$CONTAINER_ID"
fi

#### process positional parameters

echo_wrong_argument() {
 echo "Wrong argument for ""$1"" at position ""$2"
 exit
}

if [ "$1" = "BUILD" ]; then
    . ./docker_build.sh
elif [ -n "$1" ] && [ "$1" != "_" ]; then
  echo_wrong_argument "BUILD" "1"
fi

if [ "$2" = "LOGS" ]; then
    CONTAINER_LOGS="."
elif [ -n "$2" ] && [ "$2" != "_" ]; then
  echo_wrong_argument "LOGS" "2"
fi

####

docker run -d --network="host" --name m3-frontend m3-frontend

if [ "$CONTAINER_LOGS" = "." ]; then
  echo "### Opening container logs..."
  docker logs -f m3-frontend
fi