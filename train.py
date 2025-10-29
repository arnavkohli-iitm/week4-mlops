import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import sys
import os

# --- Configuration ---
# Set the tracking URI to our new local server
os.environ["MLFLOW_TRACKING_URI"] = "http://127.0.0.1:8081"
mlflow.set_tracking_uri("http://127.0.0.1:8081")

# MLflow experiment name
EXPERIMENT_NAME = "iris-decision-tree-tuning"
mlflow.set_experiment(EXPERIMENT_NAME)

# --- Load Data ---
if len(sys.argv) != 2:
    print("Usage: python train.py <data_path>")
    sys.exit(1)

data_path = sys.argv[1]
print(f"Loading data from {data_path}")
df = pd.read_csv(data_path)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# --- Hyperparameter Tuning (Two Experiments) ---
print("Starting MLflow runs...")

# Experiment 1: Simple model
params1 = {"max_depth": 3, "criterion": "gini", "random_state": 1}

# Experiment 2: Deeper model
params2 = {"max_depth": 10, "criterion": "entropy", "random_state": 1}

for i, params in enumerate([params1, params2]):

    # Start a new MLflow run
    with mlflow.start_run(run_name=f"run_{i+1}_depth_{params['max_depth']}") as run:
        print(f"Starting run {run.info.run_id} with params {params}")

        # Log parameters
        mlflow.log_params(params)

        # Create and train model
        model = DecisionTreeClassifier(**params)
        model.fit(X, y)

        # Evaluate (using training accuracy for simplicity)
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)

        # Log metrics
        mlflow.log_metric("train_accuracy", accuracy)

        # Log the model to MLflow Artifacts (on GCS) and Model Registry (in mlruns)
        print(f"Logging model with accuracy: {accuracy}")
        mlflow.sklearn.log_model(
            model,
            "model", # This is the artifact path
            registered_model_name="iris-model" # This registers it
        )

print("\nTraining and logging complete.")