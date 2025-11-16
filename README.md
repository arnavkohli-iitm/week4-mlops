# MLOps Week-8 Assignment: ML Security & Data Poisoning

This project investigates the impact of data poisoning on a machine learning model. The project builds on the previous CI/CD pipeline by introducing experiments as part of the CI process.

The `train.py` script is modified to "poison" the training data by overwriting features with random noise at 0%, 5%, 10%, and 50% levels. The CI pipeline automatically runs these experiments, logs all parameters and metrics to MLFlow, and uses CML to post a comparative report on new Pull Requests.

## 🛡️ New Concepts & Tools

* **Data Poisoning:** A function is added to `train.py` to programmatically overwrite a percentage of the training data with random values before training.
* **MLFlow Experiment Tracking:** The training script is parameterized to log the `poison_percent` and the resulting `validation_accuracy_clean` for each run. This allows for direct comparison of the attack's impact.
* **CML Reporting:** A new script (`scripts/generate_report.py`) queries the MLFlow server to build a Markdown comparison table, which is then posted as a PR comment by CML.

## 📂 Updated Project Structure

This structure highlights the new files added to enable the experiments and reporting.

```

├── .github/workflows/
│   ├── ci.yml          \# Modified: Runs poisoning experiments and CML report
├── scripts/
│   └── generate\_report.py \# New: Queries MLFlow and builds report
├── train.py              \# Modified: Added poisoning logic and argparse
└── ... (other files)

```

## 🤖 Updated CI Pipeline: Test & Validate

The `ci.yml` pipeline is updated to run the new validation steps:

1.  **DVC Pull:** Fetches the `iris.csv` dataset.
2.  **Run Pytest:** Runs the existing data and prediction tests.
3.  **Run Poisoning Experiments:** Executes `train.py` four separate times with `--poison_percent` set to `0.0`, `0.05`, `0.10`, and `0.50`.
4.  **Generate Report:** Runs `scripts/generate_report.py` to query MLFlow and create a results table.
5.  **Post CML Comment:** Combines the `pytest` output and the poisoning report into a single comment on the PR.

## 🚀 Experiment Results

The CI pipeline automatically runs the experiments. The `validation_accuracy_clean` metric shows the model's performance on the *original, clean data* after being trained on the *poisoned data*.

The CML report posted to the PR will look similar to this:

### 🧪 Poisoning Experiment Results (Experiment: iris-decision-tree-tuning)

| Poisoning %   |   Max Depth |   Accuracy (on Clean Data) |   Accuracy (on Train Data) |
|:--------------|------------:|---------------------------:|---------------------------:|
| 0.0%          |          10 |                   1        |                   1        |
| 0.0%          |           3 |                   0.973684 |                   0.973684 |
| 5.0%          |          10 |                   1        |                   1        |
| 5.0%          |           3 |                   0.980263 |                   0.960526 |
| 10.0%         |          10 |                   0.986842 |                   1        |
| 10.0%         |           3 |                   0.980263 |                   0.960526 |
| 50.0%         |          10 |                   0.947368 |                   1        |
| 50.0%         |           3 |                   0.953947 |                   0.75     |

### Observations

As shown in the (example) results, even 5-10% poisoning causes a significant drop in accuracy. At 50% poisoning, the model's performance on clean data becomes the worst, demonstrating the critical vulnerability of the training process to data quality.
