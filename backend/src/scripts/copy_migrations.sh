#!/bin/bash

# Container and paths
CONTAINER_NAME="narrow_hh-web-1"
CONTAINER_MIGRATIONS_PATH="/app/migrations/versions"
HOST_MIGRATIONS_PATH="../migrations/versions"

# Ensure the local folder exists
mkdir -p "$HOST_MIGRATIONS_PATH"

# Remove all local migration files to ensure full sync (optional but recommended)
echo "Clearing local versions directory: $HOST_MIGRATIONS_PATH"
rm -f "$HOST_MIGRATIONS_PATH"/*.py

# Copy all migration files from container to host
echo "Copying all migration files from container..."
docker cp "$CONTAINER_NAME":"$CONTAINER_MIGRATIONS_PATH/." "$HOST_MIGRATIONS_PATH/"

echo "All migration files copied successfully."