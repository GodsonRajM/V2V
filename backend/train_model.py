import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load dataset
data = pd.read_csv("dataset.csv")

# Features
X = data[["thumb","index","middle","ring","pinky"]]

# Labels
y = data["label"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "gesture_model.pkl")

print("✅ Model trained successfully!")
print("📁 Model saved as gesture_model.pkl")