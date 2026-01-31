#!/bin/bash

echo "=== Kubernetes Setup for Quantum JV Platform ==="

# Create namespace
cat > quantum-namespace.yaml << 'NS'
apiVersion: v1
kind: Namespace
metadata:
  name: quantum-platform
  labels:
    name: quantum-platform
NS

# Create config map
cat > quantum-configmap.yaml << 'CONFIGMAP'
apiVersion: v1
kind: ConfigMap
metadata:
  name: quantum-config
  namespace: quantum-platform
data:
  NODE_ENV: "production"
  PYTHONPATH: "/app/src/python"
  QUANTUM_BACKEND: "simulator"
  API_PORT: "8000"
  FRONTEND_PORT: "3000"
  DATABASE_URL: "postgresql://quantumuser:quantumpass@quantum-database:5432/quantumdb"
  REDIS_URL: "redis://redis-cache:6379"
CONFIGMAP

# Create secrets (in real scenario, use proper secret management)
cat > quantum-secrets.yaml << 'SECRETS'
apiVersion: v1
kind: Secret
metadata:
  name: quantum-secrets
  namespace: quantum-platform
type: Opaque
stringData:
  database-password: "quantumpass"
  redis-password: "redispass"
  api-key: "your-api-key-here"
  ibm-quantum-token: "your-ibm-token"
  google-quantum-token: "your-google-token"
SECRETS

# Create deployment for quantum API
cat > quantum-api-deployment.yaml << 'API_DEPLOYMENT'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quantum-api
  namespace: quantum-platform
  labels:
    app: quantum-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: quantum-api
  template:
    metadata:
      labels:
        app: quantum-api
    spec:
      containers:
      - name: quantum-api
        image: quantum-jv-platform:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: quantum-config
        - secretRef:
            name: quantum-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /api/quantum/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/quantum/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
        - name: logs-volume
          mountPath: /app/logs
      volumes:
      - name: config-volume
        configMap:
          name: quantum-config
      - name: logs-volume
        emptyDir: {}
      restartPolicy: Always
API_DEPLOYMENT

# Create service for quantum API
cat > quantum-api-service.yaml << 'API_SERVICE'
apiVersion: v1
kind: Service
metadata:
  name: quantum-api-service
  namespace: quantum-platform
spec:
  selector:
    app: quantum-api
  ports:
  - port: 8000
    targetPort: 8000
    protocol: TCP
  type: ClusterIP
API_SERVICE

# Create frontend deployment
cat > quantum-frontend-deployment.yaml << 'FRONTEND_DEPLOYMENT'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quantum-frontend
  namespace: quantum-platform
  labels:
    app: quantum-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: quantum-frontend
  template:
    metadata:
      labels:
        app: quantum-frontend
    spec:
      containers:
      - name: quantum-frontend
        image: quantum-frontend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3000
        env:
        - name: REACT_APP_API_URL
          value: "http://quantum-api-service:8000"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
FRONTEND_DEPLOYMENT

# Create frontend service
cat > quantum-frontend-service.yaml << 'FRONTEND_SERVICE'
apiVersion: v1
kind: Service
metadata:
  name: quantum-frontend-service
  namespace: quantum-platform
spec:
  selector:
    app: quantum-frontend
  ports:
  - port: 3000
    targetPort: 3000
    protocol: TCP
  type: LoadBalancer
FRONTEND_SERVICE

# Create ingress
cat > quantum-ingress.yaml << 'INGRESS'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: quantum-ingress
  namespace: quantum-platform
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - quantum.example.com
    secretName: quantum-tls
  rules:
  - host: quantum.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: quantum-api-service
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: quantum-frontend-service
            port:
              number: 3000
INGRESS

# Create horizontal pod autoscaler
cat > quantum-hpa.yaml << 'HPA'
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: quantum-api-hpa
  namespace: quantum-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: quantum-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
HPA

echo ""
echo "Kubernetes configuration files created!"
echo ""
echo "To deploy to Kubernetes:"
echo "1. Build Docker images:"
echo "   docker build -t quantum-jv-platform ."
echo "   docker build -t quantum-frontend -f Dockerfile.frontend ."
echo ""
echo "2. Apply configurations:"
echo "   kubectl apply -f quantum-namespace.yaml"
echo "   kubectl apply -f quantum-configmap.yaml"
echo "   kubectl apply -f quantum-secrets.yaml"
echo "   kubectl apply -f quantum-api-deployment.yaml"
echo "   kubectl apply -f quantum-api-service.yaml"
echo "   kubectl apply -f quantum-frontend-deployment.yaml"
echo "   kubectl apply -f quantum-frontend-service.yaml"
echo "   kubectl apply -f quantum-ingress.yaml"
echo "   kubectl apply -f quantum-hpa.yaml"
echo ""
echo "3. Check deployment:"
echo "   kubectl get all -n quantum-platform"
