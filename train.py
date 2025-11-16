import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import sys
import os
import argparse  # New import
import numpy as np # New import

# --- Configuration ---
# Set the tracking URI to our new local server
os.environ["MLFLOW_TRACKING_URI"] = "http://34.67.159.166:8081"
mlflow.set_tracking_uri("http://34.67.159.166:8081")

# MLflow experiment name
EXPERIMENT_NAME = "iris-decision-tree-tuning"
mlflow.set_experiment(EXPERIMENT_NAME)

# --- New Poisoning Function ---
def poison_data(X, y, percentage):
    """
    Poisons a percentage of the feature data (X) with random values.
    
    Returns:
    - X_poisoned: DataFrame with poisoned features
    - y: Unchanged labels
    """
    if percentage == 0:
        return X, y

    X_poisoned = X.copy()
    n_rows, n_cols = X.shape
    n_features_to_poison = int(n_rows * n_cols * percentage)
    
    # Get min/max for realistic random numbers
    X_min, X_max = X.min().min(), X.max().max()

    # Get random row and column indices
    rows = np.random.randint(0, n_rows, n_features_to_poison)
    cols = np.random.randint(0, n_cols, n_features_to_poison)
    
    # Generate random values
    random_values = np.random.uniform(X_min, X_max, n_features_to_poison)
    
    print(f"Poisoning {n_features_to_poison} feature values ({percentage*100}%)...")
    
    # Apply poisoning
    # Use .values for efficient numpy-based assignment
    X_poisoned.values[rows, cols] = random_values
    
    return X_poisoned, y

# --- Main Training Function ---
def train(data_path, poison_percent):
    """Main training and logging function."""
    print(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # --- Apply Poisoning ---
    X_train, y_train = poison_data(X, y, poison_percent)

    # --- Hyperparameter Tuning (Two Experiments) ---
    print("Starting MLflow runs...")

    # Experiment 1: Simple model
    params1 = {"max_depth": 3, "criterion": "gini", "random_state": 1}

    # Experiment 2: Deeper model
    params2 = {"max_depth": 10, "criterion": "entropy", "random_state": 1}

    for i, params in enumerate([params1, params2]):

        # Start a new MLflow run
        run_name = f"run_{i+1}_depth_{params['max_depth']}_poison_{int(poison_percent*100)}pct"
        with mlflow.start_run(run_name=run_name) as run:
            print(f"Starting run {run.info.run_id} with params {params}")

            # --- Log parameters ---
            mlflow.log_params(params)
            mlflow.log_param("poison_percent", poison_percent) # Log the poison level!

            # Create and train model
            model = DecisionTreeClassifier(**params)
            # Train on poisoned data
            model.fit(X_train, y_train) 

            # --- Evaluate ---
            # Evaluate on the *original clean data* to see the impact
            y_pred_clean = model.predict(X)
            accuracy_clean = accuracy_score(y, y_pred_clean)
            
            # Also log accuracy on the (potentially) poisoned training data
            y_pred_train = model.predict(X_train)
            accuracy_train = accuracy_score(y_train, y_pred_train)

            # --- Log metrics ---
            mlflow.log_metric("validation_accuracy_clean", accuracy_clean)
            mlflow.log_metric("train_accuracy", accuracy_train)

            # Log the model to MLflow Artifacts (on GCS) and Model Registry (in mlruns)
            print(f"Logging model with clean validation accuracy: {accuracy_clean}")
            mlflow.sklearn.log_model(
                model,
                "model", # This is the artifact path
                registered_model_name="iris-model" # This registers it
            )

    print(f"\nTraining and logging complete for poison_percent={poison_percent}.")

# --- New Argument Parsing ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Iris model with optional data poisoning.")
    
    parser.add_argument(
        "data_path", 
        type=str, 
        help="Path to the iris.csv data file"
    )
    parser.add_argument(
        "--poison_percent", 
        type=float, 
        default=0.0,
        help="Percentage of features to poison (e.g., 0.05 for 5%)"
    )
    
    args = parser.parse_args()

    # Run the main training function
    train(args.data_path, args.poison_percent)