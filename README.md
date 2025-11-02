# MLOps Week 6: Continuous Deployment to Kubernetes

This project expands on the Week 5 CI pipeline by adding a full **Continuous Deployment (CD)** workflow.

This pipeline containerizes the ML model's prediction API using **Docker** and automatically deploys it to the **Google Kubernetes Engine (GKE)**. It also uses **Workload Identity** to securely grant the GKE pod permissions to read the MLflow model from Google Cloud Storage.

## Overview

This MLOps pipeline now demonstrates an end-to-end workflow:

  * **CI (Week 5):** Validates data and tests code on `pull_request`.
  * **CD (Week 6):** Builds, pushes, and deploys the production API on `push` to `main`.

## 🛠️ New Tools Used

  * **FastAPI / Uvicorn:** Serves the ML model as a REST API.
  * **Docker:** Containerizes the FastAPI application.
  * **Google Artifact Registry:** Stores the built Docker container images.
  * **Google Kubernetes Engine (GKE):** Hosts the running API application.
  * **Kubernetes (k8s):** Manages the deployment, scaling, and networking of the container.
  * **Workload Identity:** Securely connects the Kubernetes pod to Google Cloud services (like GCS) without static keys.

## 📂 New Project Structure

This structure highlights the new files added for Week 6.

```
├── .github/workflows/
│   ├── ci.yml          # Week 5: DVC check & pytest
│   └── cd.yml          # Week 6: Build and Deploy to GKE
├── k8s/
│   ├── deployment.yaml   # GKE deployment spec
│   ├── service.yaml      # GKE LoadBalancer service
│   └── service-account.yaml # KSA for GCS permissions (Workload Identity)
├── Dockerfile              # Defines the API container
├── main.py                 # FastAPI application code
├── predict.py              # Model loading/prediction logic
├── requirements.txt        # Python dependencies
└── ... (other files)
```

## 🤖 CI/CD Pipeline

The project now has two distinct pipelines.

### 1\. Continuous Integration (CI)

This pipeline (from Week 5) runs on pull requests to ensure code and data quality.

  * Installs dependencies.
  * Authenticates to Google Cloud.
  * Pulls data from DVC.
  * Runs `pytest` to validate data and code.
  * Posts a test report to the pull request.

### 2\. Continuous Deployment (CD) 🚀

This new pipeline (`.github/workflows/cd.yml`) triggers on every `push` to the `main` branch and automatically deploys the live API.

Here's what it does:

1.  **Builds Image:** Uses the `Dockerfile` to build a new container image of the FastAPI application.
2.  **Pushes to Registry:** Authenticates with GCP and pushes the tagged image to **Google Artifact Registry** (`us-central1-docker.pkg.dev/...`).
3.  **Deploys to GKE:** Connects to the **Google Kubernetes Engine (GKE)** cluster (`mlops-cluster`).
4.  **Applies Manifests:** It applies all Kubernetes configuration files from the `k8s/` directory:
      * `k8s/service-account.yaml`: Creates a Kubernetes Service Account (`iris-api-ksa`) that is linked via Workload Identity to a Google Service Account (`iris-api-sa`). This is what grants the pod permission to read the model from your GCS bucket.
      * `k8s/deployment.yaml`: Tells GKE how to run the app, rolling out the new container image version.
      * `k8s/service.yaml`: Exposes the deployment to the internet via a `LoadBalancer`.
