import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load the dataset
data = pd.read_csv('PD.csv')

# Display the first few rows of the dataset
print(data.head())

# Split the dataset into features (X) and target (y)
X = data[['Value 1']]  # Features - use double brackets to create a DataFrame
y = data['Value 2']    # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Create a KNN classifier
k = 5  # You can choose an appropriate value for k
model = KNeighborsClassifier(n_neighbors=k)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
# y_pred = model.predict(X_test)

# # If you want to predict for a single value (e.g., 150)
# single_prediction = model.predict(pd.DataFrame({'Value 1': [150]}))
# print(f"Prediction for value 150: {single_prediction[0]}")
