import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

#LOAD DATASET

data = pd.read_csv("student_dataset.csv")

print("Dataset Loaded Successfully")

print("\nColumn Names:")
print(data.columns)

#REMOVE UNNECESSARY COLUMN

data = data.drop("Timestamp", axis=1)

#HANDLE MISSING VALUES

data = data.dropna()

print("\nDataset shape after cleaning:", data.shape)


#ENCODE CATEGORICAL DATA

le = LabelEncoder()

for col in data.columns:
    if data[col].dtype == "object":
        data[col] = le.fit_transform(data[col])

#CREATE BURNOUT SCORE

# Select key burnout related columns

sleep_hours = data["4. On average, how many hours of sleep do you get on a typical day?"]

fatigue = data["8. How often do you feel fatigued during the day, affecting your ability to study or attend classes?"]

stress = data["14. How would you describe your stress levels related to academic workload?"]

device_usage = data["11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?"]


# create burnout score formula

burnout_score = (
    0.35 * stress +
    0.30 * fatigue +
    0.20 * device_usage +
    0.15 * (8 - sleep_hours)
)

data["burnout_score"] = burnout_score

#SPLIT FEATURES & TARGET

X = data.drop("burnout_score", axis=1)
y = data["burnout_score"]


#TRAIN TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#TRAIN MODEL

model = RandomForestRegressor(n_estimators=200)

model.fit(X_train, y_train)

print("\nModel Training Completed")

# EVALUATE MODEL

pred = model.predict(X_test)

mse = mean_squared_error(y_test, pred)

print("\nModel Mean Squared Error:", mse)


#FEATURE IMPORTANCE
importance = model.feature_importances_

feature_names = X.columns

print("\nFeature Importance:")

for name, score in zip(feature_names, importance):
    print(name, ":", round(score, 3))


#SAVE MODEL

os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/burnout_model.pkl")

print("\nModel saved successfully inside /model folder")
