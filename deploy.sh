#!/bin/bash
set -e

echo "=== Updating System Packages ==="
sudo apt-get update && sudo apt-get upgrade -y

echo "=== Installing Docker & Docker Compose ==="
sudo apt-get install -y docker.io docker-compose-v2

echo "=== Setting Permissions ==="
sudo usermod -aG docker $USER

echo "=== Building & Starting Containers ==="
docker compose up -d --build

echo "=== Stack Deployment Complete ==="
docker compose ps
