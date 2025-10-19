import pytest
import pandas as pd
from predict import load_model, format_features, make_prediction

# A known sample from the Iris dataset (Iris-setosa)
# Input features: 5.1, 3.5, 1.4, 0.2
# Expected output: 'Iris-setosa' (or 0 if you label encoded it)
# We will assume your model output is 'Iris-setosa' for this example.
# **CHANGE THIS if your model outputs a number (e.g., 0).**
KNOWN_INPUT = ["5.1", "3.5", "1.4", "0.2"]
KNOWN_OUTPUT = "setosa"

@pytest.fixture
def model():
    """Fixture to load the model once for all tests."""
    m = load_model()
    if m is None:
        pytest.skip("Model file not found. Run 'dvc pull'.")
    return m

def test_model_loading(model):
    """Test that the model fixture loaded correctly."""
    assert model is not None

def test_feature_formatting():
    """Test the feature formatting function."""
    data_df = format_features(KNOWN_INPUT)
    assert isinstance(data_df, pd.DataFrame)
    assert data_df.shape == (1, 4) # 1 row, 4 columns
    assert list(data_df.columns) == ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

def test_model_prediction(model):
    """Test the model's prediction on a known sample."""
    data_df = format_features(KNOWN_INPUT)
    prediction = make_prediction(model, data_df)

    assert prediction is not None
    assert prediction == KNOWN_OUTPUT
