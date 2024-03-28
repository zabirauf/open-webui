#!/bin/bash

image_name="open-webui"
container_name="open-webui"
host_port=3000
container_port=8080

code_execution_engine_image_name="ghcr.io/engineer-man/piston"
code_execution_engine_container_name="piston_api"
code_execution_engine_host_port=3001
code_execution_engine_container_port=2000

docker build -t "$image_name" .
docker stop "$container_name" &>/dev/null || true
docker stop "$code_execution_engine_container_name" &>/dev/null || true
docker rm "$container_name" &>/dev/null || true
docker rm "$code_execution_engine_container_name" &>/dev/null || true

docker run -d -p "$host_port":"$container_port" \
    --add-host=host.docker.internal:host-gateway \
    -v "${image_name}:/app/backend/data" \
    --name "$container_name" \
    --restart always \
    "$image_name"

docker run \
    --tmpfs /piston/jobs \
    -d \
    -p "$code_execution_engine_host_port":"$code_execution_engine_container_port"\
    --name "$code_execution_engine_container_name" \
    --restart always \
    "$code_execution_engine_image_name"

docker image prune -f
