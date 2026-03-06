import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load dataset
data = pd.read_csv("../data/dataset.csv")

# Features
X = data[["thumb", "index", "middle", "ring", "pinky"]]

# Labels
y = data["label"]

# Train model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "../backend/gesture_model.pkl")

print("✅ Model trained successfully!")
print("📁 Model saved as gesture_model.pkl")