# Docker Deployment Guide
## Revolutionary AI-Powered Observability Agent with Quantum Analytics - Cross-Platform Deployment

### Quick Start with Docker

#### Development Mode (Fastest)
```bash
# Clone and navigate to project
git clone https://github.com/devkdas/AI-Observability-Agent.git
cd AI-Observability-Agent

# Edit .env with your API keys

# Run development container
docker-compose -f docker-compose.dev.yml up --build
```

#### Production Mode (Full Stack)
```bash
# Run full production stack
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f observability-agent
```

---

### Available Docker Configurations

| File | Purpose | Services |
|------|---------|----------|
| `docker-compose.dev.yml` | Development | Agent only |
| `docker-compose.yml` | Production | Agent + PostgreSQL + Redis + Nginx |

---

### Build and Run Commands

#### Build Docker Image
```bash
# Build the image
docker build -t ai-observability-agent .

# Run single container
docker run -p 8000:8000 --env-file .env ai-observability-agent
```

#### Development with Live Reload
```bash
# Development mode with volume mounting
docker-compose -f docker-compose.dev.yml up --build

# Access advanced dashboard at: http://localhost:8000/advanced-dashboard
```

#### Production Deployment
```bash
# Start all services
docker-compose up -d

# Scale the application
docker-compose up --scale observability-agent=3 -d

# Access via Nginx at: http://localhost
```

---

### Environment Configuration

Create `.env` file with required variables:

```bash
# Copado Configuration
COPADO_AI_API_KEY=your_api_key_here
COPADO_CICD_API_KEY=your_cicd_key_here

# Quantum Analytics Configuration
QUANTUM_CACHE_SIZE=1000
ML_MODEL_PATH=/app/ml_models
ENABLE_QUANTUM_ANALYTICS=true

# Database (Production)
POSTGRES_DB=observability_agent
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password_here

# Application
DEBUG=false
```

---

### Service Health Checks

All services include health checks:

```bash
# Check service health
docker-compose ps

# View health check logs
docker inspect --format='{{json .State.Health}}' ai-observability-agent
```

---

### Troubleshooting

#### Common Issues

**Port Already in Use:**
```bash
# Check what's using port 8000
netstat -tulpn | grep 8000

# Use different port
docker run -p 8001:8000 ai-observability-agent
```

**Permission Issues:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER ./data ./logs
```

**Database Connection:**
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Connect to database
docker-compose exec postgres psql -U postgres -d observability_agent
```

---

### Production Deployment Tips

#### Security
- Use Docker secrets for sensitive data
- Run containers as non-root user (already configured)
- Enable firewall rules for exposed ports

#### Performance
- Use multi-stage builds (already implemented)
- Configure resource limits in docker-compose.yml
- Use external database for high-volume deployments

#### Monitoring
```bash
# Monitor resource usage
docker stats

# View application logs
docker-compose logs -f --tail=100 observability-agent
```

---

### Cross-Platform Compatibility

This Docker setup works on:
- **Linux** (Ubuntu, CentOS, RHEL, etc.)
- **macOS** (Intel and Apple Silicon)
- **Windows** (Docker Desktop)
- **Cloud Platforms** (AWS, GCP, Azure)
- **Kubernetes** (with minor modifications)

---

### What's Included

**Revolutionary Dockerfile Features:**
- Multi-stage build optimized for quantum analytics
- Quantum cache and ML model directories
- Non-root user for enterprise security
- Advanced health checks for 4-engine AI ensemble
- Optimized dependencies for quantum processing

**Advanced Docker Compose Features:**
- Quantum analytics development and production modes
- Persistent volumes for ML models and quantum cache
- Redis for quantum analytics caching
- PostgreSQL for incident and analytics data
- Nginx reverse proxy with quantum analytics support

**Production Ready Innovation:**
- Quantum-inspired processing capabilities
- 4-engine AI ensemble containerization
- Advanced ML predictor with ensemble learning
- Real-time analytics with Chart.js/D3.js support
- Scalable architecture for 2000+ events/minute

This revolutionary Docker setup ensures your quantum-inspired AI observability solution runs consistently across all platforms with breakthrough performance!
