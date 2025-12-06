#!/bin/bash

# Deployment script for Physical AI & Humanoid Robotics Textbook System

set -e  # Exit on any error

echo "Starting deployment of Physical AI & Humanoid Robotics Textbook System..."

# Check if required environment variables are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set"
    exit 1
fi

# Build and start the services
echo "Building and starting services..."
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 10

# Check if backend is healthy
echo "Checking backend health..."
for i in {1..30}; do
    if curl -f http://localhost:8000/healthz > /dev/null 2>&1; then
        echo "Backend is healthy!"
        break
    else
        echo "Waiting for backend to be healthy... ($i/30)"
        sleep 10
    fi

    if [ $i -eq 30 ]; then
        echo "Error: Backend did not become healthy within the expected time"
        exit 1
    fi
done

# Check if Qdrant is healthy
echo "Checking Qdrant health..."
for i in {1..30}; do
    if curl -f http://localhost:6333/healthz > /dev/null 2>&1; then
        echo "Qdrant is healthy!"
        break
    else
        echo "Waiting for Qdrant to be healthy... ($i/30)"
        sleep 10
    fi

    if [ $i -eq 30 ]; then
        echo "Error: Qdrant did not become healthy within the expected time"
        exit 1
    fi
done

# Run initial content ingestion if docs directory is not empty
if [ -d "./docs" ] && [ "$(ls -A ./docs)" ]; then
    echo "Ingesting initial content..."
    sleep 5  # Give the services a bit more time to fully initialize
    docker-compose -f docker-compose.prod.yml exec backend python ingest.py

    if [ $? -eq 0 ]; then
        echo "Content ingestion completed successfully!"
    else
        echo "Warning: Content ingestion failed, but deployment continues"
    fi
else
    echo "No content found in docs directory to ingest"
fi

echo "Deployment completed successfully!"
echo "Services are running:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "Next steps:"
echo "- Access the backend API at http://localhost:8000"
echo "- To view logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "- To stop services: docker-compose -f docker-compose.prod.yml down"