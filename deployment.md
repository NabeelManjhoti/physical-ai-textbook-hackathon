# Deployment Guide for Physical AI & Humanoid Robotics Textbook System

## Overview

This guide provides instructions for deploying the Physical AI & Humanoid Robotics Textbook System to production.

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key
- Domain name and SSL certificate (if using HTTPS)
- At least 2GB of RAM available for the services

## Environment Setup

1. Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   QDRANT_API_KEY=your_qdrant_key_here  # Optional, leave empty if not using authentication
   ```

2. Ensure your textbook content is in the `docs/` directory in markdown format.

## Deployment Methods

### Method 1: Using the Deployment Script (Recommended)

1. Make the deployment script executable:
   ```bash
   chmod +x scripts/deploy.sh
   ```

2. Run the deployment script:
   ```bash
   ./scripts/deploy.sh
   ```

### Method 2: Manual Deployment

1. Build and start the services:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

2. Wait for services to be healthy (check logs with `docker-compose -f docker-compose.prod.yml logs -f`)

3. Run the ingestion script to load textbook content:
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend python ingest.py
   ```

## Service Configuration

- **Backend API**: Runs on port 8000, accessible at `http://your-domain:8000`
- **Qdrant**: Runs on port 6333, internal only (not exposed externally)
- **Memory limits**: Backend limited to 1GB, with 512MB reservation

## Health Checks

- Backend health: `GET http://your-domain:8000/healthz`
- Qdrant health: `GET http://your-domain:6333/healthz`

## SSL/HTTPS Configuration

To enable SSL/HTTPS, you can add a reverse proxy like nginx in front of the services. Here's an example nginx configuration:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring and Logging

### Docker Logs
```bash
# View all service logs
docker-compose -f docker-compose.prod.yml logs

# Follow logs in real-time
docker-compose -f docker-compose.prod.yml logs -f

# View logs for specific service
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs qdrant
```

### Resource Monitoring
```bash
# Monitor container resource usage
docker stats
```

## Troubleshooting

### Common Issues

1. **Backend not starting**: Check that `OPENAI_API_KEY` is properly set in the environment
2. **Qdrant not starting**: Ensure sufficient disk space is available for vector storage
3. **Content ingestion failing**: Verify that markdown files are in the `docs/` directory and are properly formatted

### Checking Service Status
```bash
# Check running services
docker-compose -f docker-compose.prod.yml ps

# Check specific service logs
docker-compose -f docker-compose.prod.yml logs <service-name>
```

## Updating the System

1. Pull the latest code changes
2. Rebuild the services:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

## Backup and Recovery

### Qdrant Data Backup
Qdrant data is stored in the `qdrant_data_prod` volume. To backup:
```bash
docker run --rm -v qdrant_data_prod:/data -v $(pwd):/backup alpine tar czf /backup/qdrant-backup-$(date +%Y%m%d).tar.gz -C /data .
```

### Restoring Backup
```bash
docker stop textbook-system_qdrant_1
docker run --rm -v qdrant_data_prod:/data -v $(pwd):/backup alpine tar xzf /backup/your-backup-file.tar.gz -C /data
docker start textbook-system_qdrant_1
```

## Scaling Considerations

- For higher traffic, consider adding a load balancer and running multiple backend instances
- Qdrant can be scaled horizontally in cluster mode for very large datasets
- Monitor memory usage, as the embedding model requires significant RAM

## Uninstalling

To stop and remove all services:
```bash
docker-compose -f docker-compose.prod.yml down -v
```

This will stop all containers and remove the persistent volumes (including Qdrant data).