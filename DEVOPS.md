# CityFix DevOps Documentation

Complete guide for deploying and managing the CityFix platform.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Development](#docker-development)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Git Hooks](#git-hooks)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Postman Testing](#postman-testing)
7. [Monitoring & Logging](#monitoring--logging)

---

## Local Development

### Prerequisites

- Node.js 20+
- Python 3.11+
- MongoDB 7.0+
- Git

### Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd CityFix
   ```

2. **Install Git Hooks**
   ```bash
   chmod +x local_hooks/*
   cp local_hooks/pre-commit .git/hooks/
   cp local_hooks/pre-push .git/hooks/
   cp local_hooks/commit-msg .git/hooks/
   cp local_hooks/post-merge .git/hooks/
   ```

3. **Frontend Setup**
   ```bash
   cd src/CityFixUI
   npm install
   npm run dev
   ```

4. **Backend Setup**
   ```bash
   # For each service
   cd src/AuthService  # or any other service
   pip install -r requirements.txt
   python main.py
   ```

---

## Docker Development

### Quick Start

```bash
# Development mode with hot reload
docker-compose -f docker-compose.dev.yml up --build

# Production mode
docker-compose up --build -d
```

### Development Features

- **Hot Reload**: Code changes automatically reflected
- **Volume Mounts**: Local code mounted into containers
- **Debugging**: Ports exposed for debugging
- **Isolated Environment**: Consistent across team

### Available Services

| Service              | Port  | Dev Port |
|---------------------|-------|----------|
| Frontend            | 80    | 5173     |
| Orchestrator        | 8000  | 8000     |
| Auth Service        | 8001  | 8001     |
| Admin Service       | 8002  | 8002     |
| Ticket Service      | 8003  | 8003     |
| Media Service       | 8004  | 8004     |
| Geo Service         | 8005  | 8005     |
| Notification Service| 8006  | 8006     |
| MongoDB             | 27017 | 27017    |

### Docker Commands

```bash
# Build all services
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f [service-name]

# Stop all services
docker-compose down

# Remove volumes (clean slate)
docker-compose down -v

# Rebuild single service
docker-compose up -d --build auth-service
```

---

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured
- NGINX Ingress Controller
- (Optional) Metrics Server for HPA

### Quick Deploy

```bash
# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Deploy secrets (UPDATE FIRST!)
kubectl apply -f kubernetes/secret.yaml

# Deploy configuration
kubectl apply -f kubernetes/configmap.yaml

# Deploy persistent volumes
kubectl apply -f kubernetes/pvc.yaml

# Deploy MongoDB
kubectl apply -f kubernetes/statefulset.yaml

# Deploy application services
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

# Deploy ingress
kubectl apply -f kubernetes/ingress.yaml

# Deploy autoscaling
kubectl apply -f kubernetes/hpa.yaml
```

### Verify Deployment

```bash
# Check all resources
kubectl get all -n cityfix

# Check pod status
kubectl get pods -n cityfix -w

# Check logs
kubectl logs -f deployment/orchestrator -n cityfix

# Check ingress
kubectl get ingress -n cityfix
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment orchestrator --replicas=5 -n cityfix

# Auto-scaling (via HPA)
kubectl get hpa -n cityfix
```

See `kubernetes/README.md` for detailed instructions.

---

## Git Hooks

### Local Hooks

Located in `local_hooks/`:

- **pre-commit**: Linting, formatting, security checks
- **pre-push**: Tests, builds, validation
- **commit-msg**: Conventional Commits validation
- **post-merge**: Dependency updates

### Remote Hooks

Located in `remote_hooks/`:

- **pre-receive**: Server-side validation
- **post-receive**: CI/CD triggers, notifications
- **update**: Branch protection

### Installation

```bash
# Local hooks
chmod +x local_hooks/*
cp local_hooks/* .git/hooks/

# Remote hooks (on Git server)
cp remote_hooks/* /path/to/repo.git/hooks/
chmod +x /path/to/repo.git/hooks/*
```

### Commit Message Format

```
<type>(<scope>): <subject>

Examples:
feat: add user profile page
fix(auth): resolve token expiration
docs: update API documentation
```

See `local_hooks/README.md` for details.

---

## CI/CD Pipeline

### Jenkins Pipeline

The `Jenkinsfile` defines the complete CI/CD pipeline:

#### Stages

1. **Checkout**: Clone repository
2. **Build**: Build frontend and backend
3. **Test**: Run unit and integration tests
4. **Lint**: Code quality checks
5. **Docker Build**: Build container images
6. **Docker Push**: Push to registry
7. **Deploy**: Deploy to Kubernetes
8. **Smoke Tests**: Post-deployment validation
9. **Notify**: Send notifications

#### Parameters

- `ENVIRONMENT`: dev, staging, production
- `SKIP_TESTS`: Skip test execution
- `DEPLOY`: Deploy after build

#### Required Credentials

Configure in Jenkins:

- `docker-registry-url`: Docker registry URL
- `docker-credentials`: Docker login credentials
- `k8s-config`: Kubernetes config file
- `slack-webhook-url`: Slack webhook for notifications

#### Triggering Builds

```bash
# Manual trigger
Jenkins UI → Build with Parameters

# Webhook trigger (from Git)
POST https://jenkins.example.com/generic-webhook-trigger/invoke
```

### GitHub Actions Alternative

Create `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: docker-compose build
      - name: Test
        run: npm test
      - name: Deploy
        run: kubectl apply -f kubernetes/
```

---

## Postman Testing

### Import Collection

1. Open Postman
2. Import `postman/CityFix-API.postman_collection.json`
3. Import `postman/CityFix-Environment.postman_environment.json`
4. Select environment
5. Run requests

### Newman CLI

Run from command line:

```bash
npm install -g newman

newman run postman/CityFix-API.postman_collection.json \
  -e postman/CityFix-Environment.postman_environment.json \
  --reporters cli,json,html
```

### Integration Tests

```bash
# Run collection as integration test
newman run postman/CityFix-API.postman_collection.json \
  --environment postman/CityFix-Environment.postman_environment.json \
  --bail
```

See `postman/README.md` for details.

---

## Monitoring & Logging

### Prometheus + Grafana

1. **Install Prometheus Operator**
   ```bash
   helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
   ```

2. **Configure ServiceMonitor**
   ```yaml
   apiVersion: monitoring.coreos.com/v1
   kind: ServiceMonitor
   metadata:
     name: cityfix-metrics
     namespace: cityfix
   spec:
     selector:
       matchLabels:
         app: orchestrator
     endpoints:
     - port: http
       path: /metrics
   ```

3. **Access Grafana**
   ```bash
   kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
   # Visit: http://localhost:3000
   ```

### ELK Stack (Logging)

1. **Install Elasticsearch**
   ```bash
   helm install elasticsearch elastic/elasticsearch -n logging
   ```

2. **Install Filebeat**
   ```bash
   helm install filebeat elastic/filebeat -n logging
   ```

3. **Install Kibana**
   ```bash
   helm install kibana elastic/kibana -n logging
   ```

### Application Metrics

FastAPI services expose `/metrics` endpoint:

```python
from prometheus_client import Counter, Histogram

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
```

---

## Backup & Disaster Recovery

### MongoDB Backup

```bash
# Manual backup
kubectl exec -it mongodb-0 -n cityfix -- mongodump --out /backup

# Automated backup (CronJob)
kubectl apply -f - <<EOF
apiVersion: batch/v1
kind: CronJob
metadata:
  name: mongodb-backup
  namespace: cityfix
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: mongo:7.0
            command:
            - /bin/bash
            - -c
            - mongodump --host mongodb --out /backup/\$(date +%Y%m%d)
            volumeMounts:
            - name: backup
              mountPath: /backup
          volumes:
          - name: backup
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
EOF
```

### Media Files Backup

```bash
# Sync to S3 or similar
kubectl create job --from=cronjob/media-backup media-backup-manual -n cityfix
```

---

## Troubleshooting

### Common Issues

#### Pods Not Starting

```bash
kubectl describe pod <pod-name> -n cityfix
kubectl logs <pod-name> -n cityfix
```

#### Service Connection Issues

```bash
kubectl get endpoints -n cityfix
kubectl run debug --image=curlimages/curl -it --rm -n cityfix -- curl http://orchestrator:8000/health
```

#### Database Connection

```bash
kubectl exec -it mongodb-0 -n cityfix -- mongosh -u admin -p changeme123
```

### Health Checks

All services expose `/health` endpoint:

```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
# etc.
```

---

## Security Best Practices

1. **Secrets Management**
   - Use Kubernetes Secrets
   - Consider Vault or AWS Secrets Manager
   - Never commit secrets to Git

2. **Network Policies**
   - Implement pod-to-pod restrictions
   - Use NetworkPolicies

3. **RBAC**
   - Define roles and service accounts
   - Principle of least privilege

4. **Container Security**
   - Scan images for vulnerabilities
   - Use minimal base images
   - Run as non-root user

5. **TLS/SSL**
   - Use cert-manager for certificates
   - Enforce HTTPS in ingress

---

## Performance Optimization

### Frontend

- Enable Vite build optimizations
- Use CDN for static assets
- Implement code splitting
- Enable compression (gzip/brotli)

### Backend

- Use connection pooling
- Implement caching (Redis)
- Optimize database queries
- Use async operations

### Database

- Create appropriate indexes
- Monitor slow queries
- Implement read replicas
- Use sharding for scale

---

## Support & Resources

- **Documentation**: `/docs` endpoints on each service
- **Logs**: `kubectl logs -f <pod-name> -n cityfix`
- **Metrics**: Grafana dashboards
- **Issues**: GitHub Issues or project tracker

---

## License

See LICENSE file in project root.
