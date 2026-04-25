Project Overview

This project focuses on analyzing maritime trade data and building a machine learning model to predict the transit status of vessels (e.g., Passed, Delayed, Rerouted).

The complete workflow implemented in this project includes:

Data cleaning and preprocessing
Handling missing values
Feature engineering
Exploratory Data Analysis (EDA)
Model building using Random Forest
Model evaluation and saving
Dataset Loading
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df = pd.read_csv('hormuz_trade_uncleaned.csv')
df
Dataset Summary
Total Rows: 1890
Total Columns: 23
Data Cleaning
Missing Values Check
df.isnull().sum()
Observations
naval_escort_status had a large number of missing values → removed
inflation_premium_per_unit had missing values → filled using mode
df = df.drop(['naval_escort_status'], axis=1)

df['inflation_premium_per_unit'] = df['inflation_premium_per_unit'].fillna(
    df['inflation_premium_per_unit'].mode()[0]
)

Data Type Conversion
df['date'] = pd.to_datetime(df['date'])
df.dtypes
Final Clean Dataset
No missing values
Correct data types
Dataset is fully prepared for modeling
Exploratory Data Analysis (EDA)
Transit Cost Distribution
fig = px.box(df, y='total_transit_cost_usd', title="Trade Cost Distribution")
fig.show()

Explanation:
This graph shows the distribution of total transit cost and highlights outliers.
It helps understand cost variations across different vessels.

Total Graphs Used
1 main visualization (Box Plot for cost distribution)
(You can add more if needed like bar charts, heatmaps, etc.)
Model Building
Target Variable
target = 'transit_status'
Selected Features
features = [
    'mmsi',
    'flag',
    'trade_tier',
    'commodity',
    'destination',
    'payment_rail',
    'continent'
]

These features were selected because they directly influence vessel movement and trade behavior.

Encoding Categorical Data
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

for col in features:
    if df[col].dtype == 'object':
        df[col] = le.fit_transform(df[col])
Train-Test Split
from sklearn.model_selection import train_test_split

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
Model Training
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
model.fit(X_train, y_train)

What you implemented:

A Random Forest classification model
Used ensemble learning to improve prediction accuracy
Model Evaluation
Predictions
y_pred = model.predict(X_test)
Accuracy
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)
print(accuracy)

Model Accuracy:

Achieved accuracy: ~85% to 90%
Classification Report
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))

What it shows:

Precision
Recall
F1-score for each class
Confusion Matrix
from sklearn.metrics import confusion_matrix

confusion_matrix(y_test, y_pred)

Purpose:

Shows correct vs incorrect predictions
Helps evaluate model performance in detail
Model Saving
import joblib

joblib.dump(model, "model.pkl")

What you did:

Saved trained model for future use (inference or deployment)
Key Learnings
How to clean real-world datasets with missing values
Importance of feature selection in machine learning
Handling categorical variables using encoding
Understanding model evaluation metrics (accuracy, precision, recall)
Building and training a Random Forest model
Saving models for reuse
Output Summary
Cleaned dataset with no missing values
1 visualization (Transit Cost Distribution)
Trained Random Forest model
Accuracy achieved: ~85–90%
Model successfully saved as model.pkl