# Monitoring Guide for Physical AI & Humanoid Robotics Textbook System

## Overview

This document outlines the monitoring strategy and practices for the Physical AI & Humanoid Robotics Textbook System to ensure optimal performance and availability.

## Health Checks

### Backend Service
- **Endpoint**: `GET /healthz`
- **Expected Response**: `{"status": "healthy", "service": "textbook-backend"}`
- **Frequency**: Every 30 seconds (configured in docker-compose)
- **Purpose**: Verify that the backend application is running and responding

### Qdrant Service
- **Endpoint**: `GET /healthz`
- **Expected Response**: `{"title": "qdrant - vector database", "version": "x.x.x"}`
- **Frequency**: Every 30 seconds (configured in docker-compose)
- **Purpose**: Verify that the vector database is running and accessible

## Key Metrics to Monitor

### Backend Metrics
- **Response Time**: Target <200ms for chat queries
- **Error Rate**: Should remain <1%
- **Throughput**: Requests per second
- **CPU Usage**: Should not consistently exceed 80%
- **Memory Usage**: Monitor for potential leaks, especially with embedding model

### Qdrant Metrics
- **Vector Storage Size**: Monitor growth over time
- **Query Performance**: Vector search response times
- **Disk Usage**: Storage for vector embeddings
- **Index Performance**: Search efficiency

### Application-Specific Metrics
- **Chat Query Volume**: Number of queries per time period
- **Ingestion Success Rate**: Percentage of successful content ingestion
- **Content Relevance**: Quality of responses based on textbook content

## Logging Strategy

### Log Levels
- **ERROR**: Critical issues that affect service availability
- **WARN**: Issues that may impact functionality but don't stop the service
- **INFO**: General operational information (requests, startup, shutdown)
- **DEBUG**: Detailed information for troubleshooting (not enabled in production)

### Log Locations
- **Docker Logs**: Accessible via `docker logs <container_name>`
- **Application Logs**: Structured logs output to stdout/stderr
- **Qdrant Logs**: Internal to the Qdrant container

### Log Retention
- Docker logs are rotated automatically
- Consider external log aggregation for long-term storage and analysis

## Alerting Configuration

### Critical Alerts
- Backend service unavailable
- Qdrant database unavailable
- High error rates (>5% for 5+ minutes)
- Memory usage >90% for 10+ minutes

### Warning Alerts
- Response times >500ms for 5+ minutes
- CPU usage >80% for 15+ minutes
- Disk usage >80% for 10+ minutes

## Monitoring Tools Integration

### Docker-based Monitoring
```bash
# Monitor container resource usage
docker stats

# View logs in real-time
docker-compose -f docker-compose.prod.yml logs -f

# Monitor specific container
docker stats <container_name>
```

### Custom Monitoring Endpoints
The system includes health check endpoints that can be integrated with monitoring tools:
- Backend: `http://your-domain:8000/healthz`
- Qdrant: `http://your-domain:6333/healthz`

## Performance Monitoring

### Baseline Performance
- **Chat Response Time**: <200ms for 95% of requests
- **Content Ingestion**: <5s for documents under 100KB
- **Vector Search**: <100ms for similarity search

### Performance Testing
Regular performance testing should include:
- Load testing with concurrent users
- Stress testing to identify breaking points
- End-to-end functionality testing

## Troubleshooting Common Issues

### Slow Response Times
1. Check Qdrant performance metrics
2. Verify sufficient memory allocation
3. Review embedding model resource usage
4. Check for database index issues

### High Error Rates
1. Verify API key validity (OpenAI, Qdrant)
2. Check network connectivity between services
3. Review application logs for specific error details
4. Check rate limits on external APIs

### Ingestion Failures
1. Verify source markdown files are accessible
2. Check file format and encoding
3. Verify Qdrant write permissions
4. Review chunking service logs

## Maintenance Tasks

### Regular Maintenance
- **Daily**: Review logs for errors or unusual patterns
- **Weekly**: Check disk space and resource usage
- **Monthly**: Review performance metrics trends

### Preventive Measures
- Regular backup of Qdrant data
- Monitoring of external API usage (OpenAI)
- Keeping dependencies up to date
- Performance testing after updates

## Incident Response

### Response Procedures
1. **Detection**: Automated alerts or user reports
2. **Assessment**: Check logs and metrics to identify root cause
3. **Mitigation**: Apply appropriate fix or workaround
4. **Communication**: Notify stakeholders if service is affected
5. **Resolution**: Implement permanent fix
6. **Review**: Document incident and update procedures

### Rollback Procedures
If a deployment causes issues:
```bash
# Roll back to previous version
docker-compose -f docker-compose.prod.yml down
# Revert code changes
git checkout <previous-commit>
# Rebuild and deploy
./scripts/deploy.sh
```

## Security Monitoring

### Access Monitoring
- Monitor API key usage patterns
- Log authentication failures
- Track unusual query patterns

### Data Security
- Monitor access to sensitive data
- Verify proper data handling in logs
- Regular security scanning of dependencies