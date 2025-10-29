import joblib
import sys
import pandas as pd

MODEL_PATH = 'artifacts/model.joblib'

import joblib
import sys
import pandas as pd
import os
import mlflow.pyfunc

# New Model Loading Function
def load_model():
    """
    Loads the latest 'iris-model' from the self-hosted MLflow server.
    """
    print("Connecting to MLflow server at http://127.0.0.1:8081...")
    try:
        # Set the tracking URI to our local server
        mlflow.set_tracking_uri("http://127.0.0.1:8081")

        model_name = "iris-model"

        # Load the latest version of the model
        model_uri = f"models:/{model_name}/latest" 

        print(f"Loading model '{model_name}' (latest) from MLflow Registry...")
        model = mlflow.pyfunc.load_model(model_uri)
        print("Model loaded successfully.")
        return model

    except Exception as e:
        print(f"Error loading model from MLflow Registry: {e}")
        print("Did you run the training script to register a model?")
        return None

def format_features(features):
    """Formats a list of feature strings into a DataFrame."""
    try:
        # Convert string inputs to floats
        feature_values = [float(f) for f in features]
        
        # Create a DataFrame with the correct feature names
        column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        data_df = pd.DataFrame([feature_values], columns=column_names)
        return data_df
        
    except Exception as e:
        print(f"Error: Invalid input features. Expected 4 numbers. Got: {features}")
        print(e)
        return None

def make_prediction(model, data_df):
    """Makes a prediction using the loaded model and formatted data."""
    if model is None or data_df is None:
        return None
    
    # Make prediction
    prediction = model.predict(data_df)
    return prediction[0] # Return the single prediction value

def main():
    """Main function to run the script from the command line."""
    if len(sys.argv) != 5:
        print("Usage: python predict.py <sepal_length> <sepal_width> <petal_length> <petal_width>")
        print("Example: python predict.py 5.1 3.5 1.4 0.2")
        return

    features = sys.argv[1:]
    model = load_model()
    
    if model:
        data_df = format_features(features)
        if data_df is not None:
            prediction = make_prediction(model, data_df)
            if prediction is not None:
                print(f"Prediction: {prediction}")

if __name__ == "__main__":
    main()