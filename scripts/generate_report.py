import mlflow
import os
import pandas as pd

# Set the tracking URI
MLFLOW_TRACKING_URI = "http://34.67.159.166:8081"
os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

EXPERIMENT_NAME = "iris-decision-tree-tuning"

def fetch_results_and_print_report():
    """
    Fetches the latest experiment runs and prints a Markdown report.
    """
    try:
        experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
        if not experiment:
            print(f"Error: Experiment '{EXPERIMENT_NAME}' not found.")
            return

        # Fetch all runs from this experiment
        runs_df = mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["start_time DESC"]
        )
        
        if runs_df.empty:
            print("No runs found in experiment.")
            return

        # Filter for the relevant parameters and metrics
        relevant_cols = [
            "params.poison_percent",
            "params.max_depth",
            "metrics.validation_accuracy_clean",
            "metrics.train_accuracy"
        ]
        
        # Ensure columns exist before trying to access them
        cols_to_use = [col for col in relevant_cols if col in runs_df.columns]
        report_df = runs_df[cols_to_use]

        # We ran 4 poison levels * 2 model types = 8 runs
        # Let's just grab the most recent 8 runs for this report
        report_df = report_df.head(8).sort_values(by="params.poison_percent")
        
        # Rename for better table headers
        report_df.rename(columns={
            "params.poison_percent": "Poisoning %",
            "params.max_depth": "Max Depth",
            "metrics.validation_accuracy_clean": "Accuracy (on Clean Data)",
            "metrics.train_accuracy": "Accuracy (on Train Data)"
        }, inplace=True)
        
        # Format the poisoning %
        if "Poisoning %" in report_df.columns:
            report_df["Poisoning %"] = (report_df["Poisoning %"].astype(float) * 100).astype(str) + "%"

        # --- Print Markdown Report ---
        print(f"### 🧪 Poisoning Experiment Results (Experiment: {EXPERIMENT_NAME})\n")
        print(report_df.to_markdown(index=False))

    except Exception as e:
        print(f"An error occurred while generating the report: {e}")

if __name__ == "__main__":
    fetch_results_and_print_report()