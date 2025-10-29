# MLOps Week 5 Assignment: MLflow + Homework Pipeline

This project demonstrates a complete MLOps workflow. It uses **DVC** for data versioning, **MLflow** for experiment tracking and model registry, and **GitHub Actions** for CI/CD.

## Overview

The project trains a `DecisionTreeClassifier` on the Iris dataset. The key goal is the MLOps pipeline built around it.

This pipeline automatically:
* Versions the training data using **DVC** with a Google Cloud Storage (GCS) remote.
* Runs hyperparameter tuning experiments and logs them using a local **MLflow** server.
* Registers the trained models to the MLflow Model Registry.
* Separates training and inference logic into distinct scripts.
* Validates data using **Pytest**.
* Runs an automated CI/CD pipeline using **GitHub Actions** on every push and pull request.
* Posts a "sanity report" (test results) as a comment on pull requests using **CML**.

## 🛠️ Tools Used

* **Python**: The core programming language.
* **scikit-learn**: For the machine learning model.
* **DVC (Data Version Control)**: To version the dataset.
* **MLflow**: For experiment tracking and model registry.
* **GCS (Google Cloud Storage)**: Used as the remote storage backend for DVC and MLflow artifacts.
* **Pytest**: For data validation and model testing.
* **GitHub Actions**: For automating the CI/CD pipeline.
* **CML (Continuous Machine Learning)**: For posting test reports back to GitHub pull requests.


## 📂 Project Structure

```

├── .github/workflows/ci.yml  \# The main CI/CD workflow
├── data/
│   └── iris.csv.dvc          \# DVC pointer to our dataset
├── tests/
│   ├── test_data_validation.py \# Pytest for checking data integrity
│   └── test_prediction.py      \# Pytest for checking model loading
├── mlruns/                   \# Local MLflow experiment tracking data
├── requirements.txt          \# Project dependencies
├── train.py                  \# Script for training and logging to MLflow
└── predict.py                \# Script for loading from MLflow Registry

```


## 🤖 CI/CD Pipeline

The workflow is defined in `.github/workflows/ci.yml` and runs automatically on every `push` and `pull_request`.

Here's what it does:

1.  **Installs** all Python dependencies, including `mlflow`.
2.  **Authenticates** with Google Cloud Storage.
3.  **Pulls Data**: Runs `dvc pull` to download the `iris.csv` dataset.
4.  **Runs Tests**: Executes the `pytest` suite. Model-loading tests are skipped since the CI runner cannot connect to our local MLflow server.
5.  **Generates Report (on PRs only)**: Generates a Markdown report (`report.md`) containing the `pytest` output.
6.  **Posts Comment (on PRs only)**: CML posts the `report.md` file as a comment on the pull request.
