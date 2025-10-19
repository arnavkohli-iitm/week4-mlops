import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
import sys

# Loading args
data_path = sys.argv[1]
model_path = sys.argv[2]

# Reading Data into df
df = pd.read_csv(data_path)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

model = DecisionTreeClassifier(max_depth=3, random_state=1)
model.fit(X, y)

joblib.dump(model, model_path)
print(f"Model saved to {model_path}")
