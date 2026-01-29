# CityFix Kubernetes Deployment

This directory contains Kubernetes manifests for deploying CityFix platform to a Kubernetes cluster.

## Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl CLI configured
- NGINX Ingress Controller installed
- (Optional) cert-manager for TLS certificates
- (Optional) Metrics Server for HPA

## Quick Start

### 1. Create Namespace

```bash
kubectl apply -f namespace.yaml
```

### 2. Create Secrets

**Important:** Update the secrets in `secret.yaml` before deploying to production!

```bash
# Edit secret.yaml with your actual secrets (base64 encoded)
kubectl apply -f secret.yaml
```

Or create secrets directly:

```bash
kubectl create secret generic cityfix-secrets \
  --from-literal=JWT_SECRET='your-super-secret-jwt-key' \
  --from-literal=MONGO_USER='admin' \
  --from-literal=MONGO_PASSWORD='your-secure-password' \
  -n cityfix
```

### 3. Create ConfigMaps

```bash
kubectl apply -f configmap.yaml
```

### 4. Create Persistent Volume Claims

```bash
kubectl apply -f pvc.yaml
```

### 5. Deploy MongoDB

```bash
kubectl apply -f statefulset.yaml
```

Wait for MongoDB to be ready:

```bash
kubectl wait --for=condition=ready pod -l app=mongodb -n cityfix --timeout=300s
```

### 6. Deploy Application Services

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 7. Deploy Ingress

Update the hostnames in `ingress.yaml` before applying:

```bash
kubectl apply -f ingress.yaml
```

### 8. (Optional) Deploy Horizontal Pod Autoscalers

Requires Metrics Server to be installed:

```bash
kubectl apply -f hpa.yaml
```

## Complete Deployment (All at Once)

```bash
kubectl apply -f namespace.yaml
kubectl apply -f secret.yaml
kubectl apply -f configmap.yaml
kubectl apply -f pvc.yaml
kubectl apply -f statefulset.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
kubectl apply -f hpa.yaml
```

## Verify Deployment

```bash
# Check all resources
kubectl get all -n cityfix

# Check pods status
kubectl get pods -n cityfix

# Check services
kubectl get svc -n cityfix

# Check ingress
kubectl get ingress -n cityfix

# Check HPA
kubectl get hpa -n cityfix

# Check logs of a specific service
kubectl logs -f deployment/orchestrator -n cityfix
```

## Access the Application

### Via Ingress (Production)

After configuring DNS and TLS:

- Frontend: https://cityfix.example.com
- API: https://api.cityfix.example.com

### Via NodePort (Development)

```bash
# Get the node IP
kubectl get nodes -o wide

# Access orchestrator on NodePort 30000
curl http://<NODE_IP>:30000/health

# Port forward for frontend
kubectl port-forward svc/frontend 8080:80 -n cityfix
# Access: http://localhost:8080
```

### Via Port Forward (Development)

```bash
# Frontend
kubectl port-forward svc/frontend 8080:80 -n cityfix

# Orchestrator
kubectl port-forward svc/orchestrator 8000:8000 -n cityfix

# MongoDB (for debugging)
kubectl port-forward svc/mongodb 27017:27017 -n cityfix
```

## Scaling

### Manual Scaling

```bash
# Scale a deployment
kubectl scale deployment orchestrator --replicas=5 -n cityfix

# Scale ticket-service
kubectl scale deployment ticket-service --replicas=10 -n cityfix
```

### Auto Scaling (HPA)

The HPA configurations will automatically scale based on CPU/memory usage:

- Orchestrator: 2-10 replicas
- Ticket Service: 3-15 replicas
- Frontend: 2-10 replicas

## Monitoring

```bash
# Watch pods
kubectl get pods -n cityfix -w

# Describe a pod
kubectl describe pod <pod-name> -n cityfix

# View logs
kubectl logs -f deployment/orchestrator -n cityfix

# View logs from all replicas
kubectl logs -f deployment/ticket-service --all-containers=true -n cityfix

# Execute commands in a pod
kubectl exec -it <pod-name> -n cityfix -- /bin/bash
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod events
kubectl describe pod <pod-name> -n cityfix

# Check pod logs
kubectl logs <pod-name> -n cityfix
```

### Service Connection Issues

```bash
# Check service endpoints
kubectl get endpoints -n cityfix

# Test service connectivity from a pod
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -n cityfix -- curl http://orchestrator:8000/health
```

### MongoDB Issues

```bash
# Check MongoDB logs
kubectl logs -f statefulset/mongodb -n cityfix

# Connect to MongoDB
kubectl exec -it mongodb-0 -n cityfix -- mongosh -u admin -p changeme123
```

### Ingress Issues

```bash
# Check ingress controller logs
kubectl logs -f -n ingress-nginx deployment/ingress-nginx-controller

# Describe ingress
kubectl describe ingress cityfix-ingress -n cityfix
```

## Updates and Rollouts

### Update an Image

```bash
# Update orchestrator image
kubectl set image deployment/orchestrator orchestrator=cityfix/orchestrator:v2.0 -n cityfix

# Check rollout status
kubectl rollout status deployment/orchestrator -n cityfix

# View rollout history
kubectl rollout history deployment/orchestrator -n cityfix
```

### Rollback a Deployment

```bash
# Rollback to previous version
kubectl rollout undo deployment/orchestrator -n cityfix

# Rollback to specific revision
kubectl rollout undo deployment/orchestrator --to-revision=2 -n cityfix
```

## Cleanup

### Delete Specific Resources

```bash
kubectl delete -f ingress.yaml
kubectl delete -f hpa.yaml
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
kubectl delete -f statefulset.yaml
```

### Delete Everything

```bash
kubectl delete namespace cityfix
```

**Warning:** This will delete all resources including persistent data!

## Production Considerations

1. **Secrets Management**: Use external secret management (HashiCorp Vault, AWS Secrets Manager, etc.)
2. **TLS Certificates**: Use cert-manager with Let's Encrypt or your own CA
3. **Backup**: Implement regular MongoDB backups using VolumeSnapshots or external tools
4. **Monitoring**: Install Prometheus and Grafana for metrics
5. **Logging**: Use ELK stack or Loki for centralized logging
6. **Resource Limits**: Adjust resource requests/limits based on actual usage
7. **Network Policies**: Implement NetworkPolicies for pod-to-pod communication
8. **Pod Security**: Use PodSecurityPolicies or Pod Security Standards
9. **High Availability**: Run MongoDB in replica set mode for production
10. **Load Balancing**: Use external load balancer for production traffic

## Helm Chart (Alternative)

For easier management, consider creating a Helm chart:

```bash
helm create cityfix
# Move these manifests to templates/
# Add values.yaml for configuration
helm install cityfix ./cityfix -n cityfix
```

## CI/CD Integration

These manifests can be deployed via CI/CD pipelines:

```yaml
# Example GitLab CI
deploy:
  stage: deploy
  script:
    - kubectl apply -f kubernetes/
  only:
    - main
```

## Support

For issues or questions, refer to the main project README or open an issue.
