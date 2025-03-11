# Deploy KEDA with RabbitMQ on Google Cloud

## Overview
This guide explains how to deploy [KEDA](https://keda.sh/) with RabbitMQ as an event source on Google Cloud Kubernetes Engine (GKE). We will:
1. Set up a GKE cluster.
2. Install KEDA.
3. Deploy RabbitMQ.
4. Create a KEDA ScaledObject to auto-scale pods.
5. Test the setup.

## Step 1: Initialize the gcloud CLI
Install Google Cloud SDK: Follow the instructions to install the Google Cloud SDK: Install SDK
Initialize the gcloud CLI
```sh
which gcloud
rm ...
./google-cloud-sdk/bin/gcloud init
gcloud --version
```
List gcloud components
```sh
gcloud components list
```
Install kubectl client
```sh
gcloud components install gke-gcloud-auth-plugin
gcloud components install kubectl
kubectl version
```

## Step 2: Create a GKE Cluster
```sh
./setup/create-gke-cluster
```

## Step 3: Install KEDA
```sh
./setup/install-keda
```

Verify KEDA installation:
```sh
kubectl get pods -n keda
```

## Step 4: Deploy a Sample Worker App
Create a `deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: keda-rabbitmq
  namespace: default
  labels:
    app: keda-rabbitmq
spec:
  replicas: 1
  selector:
    matchLabels:
      app: keda-rabbitmq
  template:
    metadata:
      labels:
        app: keda-rabbitmq
    spec:
      containers:
        - name: keda-rabbitmq
          image: IMAGE
          imagePullPolicy: Always
          envFrom:
            - secretRef:
                name: keda-rabbitmq-secret
          
          volumeMounts:
            - name: secret-volume
              mountPath: /etc/secret-volume
              readOnly: true
      volumes:
        - name: secret-volume
          secret:
            secretName: keda-rabbitmq-secret
```
Apply the deployment:
```sh
kubectl apply -f deployment.yaml
```

## Step 5: Configure KEDA ScaledObject
Create `scaledobject.yaml`:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: rabbitmq-scaledobject
  namespace: default
spec:
  scaleTargetRef:
    name: keda-rabbitmq
  minReplicaCount: 0
  maxReplicaCount: 5
  triggers:
    - type: rabbitmq
      metadata:
        protocol: amqp
        queueName: QUEUE_NAME
        mode: QueueLength
        value: "2"
      authenticationRef:
        name: rabbitmq-trigger-auth
```
Apply the configuration:
```sh
kubectl apply -f scaledobject.yaml
```

## Step 6: Test the Scaling
1. Publish messages to RabbitMQ queue:
```sh
python -m src.send
```

2. Check if the pods scale up:
```sh
kubectl get pods -w
```