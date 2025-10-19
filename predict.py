import joblib
import sys
import pandas as pd

MODEL_PATH = 'artifacts/model.joblib'

def load_model():
    """Loads the model from disk."""
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except FileNotFoundError:
        print("Error: Model file not found.")
        print("Please run 'dvc pull' to download the model from GCS.")
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