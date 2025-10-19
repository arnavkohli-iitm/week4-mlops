# MLOps Week 4 Assignment: CML + GitHub Actions + DVC

This project demonstrates a complete MLOps workflow for training and serving a machine learning model. It uses DVC for data and model versioning, GitHub Actions for CI/CD, and CML for automated reporting.

## Overview

The project trains a simple `DecisionTreeClassifier` on the Iris dataset. The key goal isn't the model itself, but the MLOps pipeline built around it.

This pipeline automatically:
* Versions the training data and the trained model using **DVC** with a Google Cloud Storage (GCS) remote.
* Separates training and inference logic into distinct scripts.
* Validates data and model performance using **Pytest**.
* Runs an automated CI/CD pipeline using **GitHub Actions** on every push and pull request.
* Posts a "sanity report" (test results + sample prediction) as a comment on pull requests using **CML**.

---

## 🛠️ Tools Used

* **Python**: The core programming language.
* **scikit-learn**: For the machine learning model.
* **DVC (Data Version Control)**: To version large files (data and models) outside of Git.
* **GCS (Google Cloud Storage)**: Used as the remote storage backend for DVC.
* **Pytest**: For data validation and model testing.
* **GitHub Actions**: For automating the CI/CD pipeline.
* **CML (Continuous Machine Learning)**: For posting test reports back to GitHub pull requests.

---

## 📂 Project Structure

```
├── .github/workflows/ci.yml  \# The main CI/CD workflow
├── data/
│   └── iris.csv.dvc          \# DVC pointer to our dataset
├── artifacts/
│   └── model.joblib.dvc    \# DVC pointer to our trained model
├── tests/
│   ├── test\_data\_validation.py \# Pytest for checking data integrity
│   └── test\_prediction.py      \# Pytest for checking model performance
├── dvc.yaml                  \# DVC pipeline definition
├── requirements.txt          \# Project dependencies
├── train.py                  \# Script for training the model
└── predict.py                \# Script for running live predictions
```

---


## 🤖 CI/CD Pipeline

The workflow is defined in `.github/workflows/ci.yml` and runs automatically on every `push` and `pull_request`.

Here's what it does:

1.  **Installs** all Python and CML dependencies.
2.  **Authenticates** with Google Cloud Storage using a repository secret.
3.  **Pulls Data**: Runs `dvc pull` to download the model and data needed for testing.
4.  **Runs Tests**: Executes the `pytest` suite. This step is allowed to fail so that the report can still be posted.
5.  **Generates Report (on PRs only)**: If the workflow was triggered by a Pull Request, it generates a Markdown report (`report.md`) containing:
      * The full `pytest` output (pass or fail).
      * The result of a "sanity check" prediction.
6.  **Posts Comment (on PRs only)**: CML posts the `report.md` file as a comment on the pull request, giving you immediate feedback on your changes.