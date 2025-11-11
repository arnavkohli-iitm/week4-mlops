# MLOps Week 7: Kubernetes Autoscaling and Stress Testing

This project expands on the Week 6 CD pipeline by introducing automatic scaling and load testing.

The pipeline now uses a **Kubernetes Horizontal Pod Autoscaler (HPA)** to automatically scale the API pods based on CPU load. The CD workflow is extended to run an automated stress test using **`wrk`** immediately after deployment to validate the scaling behavior and identify performance bottlenecks.

## 🛠️Scaling - New Concepts & Tools

* **Kubernetes HPA:** The `HorizontalPodAutoscaler` resource automatically increases or decreases the number of pods in a deployment based on observed CPU utilization.
* **`wrk`:** A high-performance HTTP benchmarking tool used to generate thousands of concurrent requests to stress test the API.
* **Lua:** Used to write a small script (`wrk-post.lua`) to enable `wrk` to send `POST` requests with a JSON body, which is required by our `/predict` endpoint.

## 📂 New Project Structure

This structure highlights the new files added to enable autoscaling and testing.

```

├── .github/workflows/
│   ├── cd.yml          \# Modified: Added wrk stress-testing steps
├── k8s/
│   ├── deployment.yaml   \# Modified: Added CPU resource requests
│   ├── hpa.yaml          \# New: Defines the Horizontal Pod Autoscaler
│   └── wrk-post.lua      \# New: Script for wrk to send POST requests
└── ... (other files)

```

## 🤖 Updated CD Pipeline: Deploy & Test

The `cd.yml` pipeline is updated with a new testing phase that runs *after* the deployment succeeds.

1.  **Builds & Pushes Image:** (No change)
2.  **Deploys to GKE:** (No change)
    * Applies all `k8s/` manifests, including the new `hpa.yaml`.
3.  **Install `wrk`:** The runner installs the `wrk` tool.
4.  **Get LoadBalancer IP:** Waits for the `iris-api-service` to get an external IP address.
5.  **Run Stress Test:** Executes `wrk` against the service IP to simulate high traffic.
6.  **Observe Autoscaling:** Runs `kubectl get hpa` to show how the HPA reacted to the load.

## 🚀 Experiment Results

The pipeline was run twice to observe two different scenarios as required.

### Experiment 1: Autoscaling (max_pods: 3)

* **Configuration:**
    * `k8s/hpa.yaml` set to `minReplicas: 1`, `maxReplicas: 3`.
    * `cd.yml` ran `wrk -c1000` (1000 concurrent connections).
* **Observation:** The HPA successfully detected the high CPU load (e.g., `250%/50%`) and scaled the number of `iris-api-deployment` pods from 1 to 3 to handle the traffic.

### Experiment 2: Bottleneck (max_pods: 1)

* **Configuration:**
    * `k8s/hpa.yaml` modified to `maxReplicas: 1`.
    * `cd.yml` modified to `wrk -c2000` (2000 concurrent connections).
* **Observation:** A bottleneck was successfully created.
    * The `wrk` test showed very high latency and a large number of socket/read errors.
    * The `kubectl get hpa` output showed the CPU target was extremely high, but the `REPLICAS` count remained **stuck at 1**, proving the HPA was constrained and could not scale out, which caused the performance bottleneck.
