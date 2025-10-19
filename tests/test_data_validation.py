import pytest
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/iris.csv")
EXPECTED_COLUMNS = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

@pytest.fixture
def data():
    """Fixture to load the dataset."""
    if not DATA_PATH.exists():
        pytest.skip("Data file not found. Run 'dvc pull'.")
    return pd.read_csv(DATA_PATH)

def test_data_file_exists():
    """Test if the data file exists."""
    assert DATA_PATH.exists(), "data/iris.csv not found. Run 'dvc pull' first."

def test_data_columns(data):
    """Test if the dataset has the expected columns."""
    assert list(data.columns) == EXPECTED_COLUMNS, "Column names do not match expected."

def test_data_no_nulls(data):
    """Test for any null (missing) values in the dataset."""
    assert data.isnull().sum().sum() == 0, "Found null values in data."

def test_data_types(data):
    """Test that feature columns are numeric."""
    for col in EXPECTED_COLUMNS[:-1]: # All columns except the last one (species)
        assert pd.api.types.is_numeric_dtype(data[col]), f"Column {col} is not numeric."
