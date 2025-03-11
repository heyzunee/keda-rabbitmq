# Project Setup and Usage Guide

## 1. Install Google Cloud SDK
Follow the instructions to install the Google Cloud SDK: [Install SDK](https://cloud.google.com/sdk/docs/install-sdk#deb)

## 2. Initialize the gcloud CLI
```sh
which gcloud
rm ...
./google-cloud-sdk/bin/gcloud init
gcloud --version
```

### List gcloud components
```sh
gcloud components list
```

### Install kubectl client
```sh
gcloud components install gke-gcloud-auth-plugin
gcloud components install kubectl
kubectl version
```

## 3. Google Cloud Storage (GCS)
### Create service account
Navigate to IAM & Admin → Service Accounts → Create service account

### Add role
Navigate to IAM → Add another role: Storage Object Admin & Storage Object Creator

### Activate service account
```sh
gcloud auth activate-service-account --key-file="/path/to/your/service-account-file.json"
```

### Set google application credentials
```sh
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
```

### Check access token
```sh
gcloud auth application-default print-access-token
```

## 4. Create GKE cluster
```sh
./create-gke-cluster
```

## 5. KEDA RabbitMQ

### Build and Push Docker Image
```sh
cd keda-rabbitmq
docker build -t keda:v1 .
docker tag keda:v1 us-east1-docker.pkg.dev/yumao-dev/my-repo/keda:v1
docker push us-east1-docker.pkg.dev/yumao-dev/my-repo/keda:v1
```

### Deploy to Kubernetes
```sh
kubectl apply -f deployment.yaml
```
