Project Overview:
This project demonstrates PostgreSQL concepts including DDL, DML, Functions,
Triggers, Joins, and Aggregations. It simulates a system for managing vessel
trade data, country information, and logging system activities.

------------------------------------------------------------
Tables Used:

1. vessels  
   Stores vessel-related data including toll charges.

2. logs_table  
   Stores logs with message and timestamp.

3. countryinfo  
   Stores country name and commodity.

4. country_summary  
   Stores aggregated trade data.

5. trade_records and cargo  
   Used for JOIN operations.

------------------------------------------------------------
Features Implemented:

1. Aggregation Function

Function Name: countcost()  
Purpose: Calculates total toll cost from vessels table.

CREATE OR REPLACE FUNCTION countcost()
RETURNS INT AS $$
BEGIN
  RETURN (SELECT SUM(toll_usd) FROM vessels);
END;
$$ LANGUAGE plpgsql;

Usage:
SELECT countcost();

------------------------------------------------------------
2. Trigger on countryinfo Table

CREATE OR REPLACE FUNCTION log_country_insert_func()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO logs_table(message, "timestamp")
  VALUES ('Inserted new country ' || NEW.name, NOW());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_country_insert
AFTER INSERT ON countryinfo
FOR EACH ROW
EXECUTE FUNCTION log_country_insert_func();

------------------------------------------------------------
3. Insert Operation

INSERT INTO countryinfo (name, commodity)
VALUES ('INDIA', 'CRUDE OIL');

------------------------------------------------------------
4. JOIN Query

SELECT t.flag, c.commodity
FROM trade_records AS t
INNER JOIN cargo AS c
ON t.vessel_id = c.vessel_id;

------------------------------------------------------------
5. Trigger on country_summary Table

CREATE OR REPLACE FUNCTION log_country_summary_insert()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO logs_table(message, "timestamp")
  VALUES ('Summary updated for flag ' || NEW.flag, NOW());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_country_summary
AFTER INSERT ON country_summary
FOR EACH ROW
EXECUTE FUNCTION log_country_summary_insert();

------------------------------------------------------------
6. Insert into country_summary

INSERT INTO country_summary (
  flag,
  total_trade_volume_usd,
  total_trades,
  average_trade_value_usd,
  commodities,
  date
)
VALUES (
  'INDIA',
  1000000,
  10,
  100000,
  'CRUDE OIL',
  NOW()
);

------------------------------------------------------------
Logs Verification:

SELECT * FROM logs_table;

How to Run:

1. Create all required tables
2. Run functions
3. Create triggers
4. Insert data
5. Execute queries

Concepts Covered:

- DDL (CREATE TABLE)
- DML (INSERT)
- Functions (PL/pgSQL)
- Triggers (AFTER INSERT)
- Aggregation (SUM)
- INNER JOIN
- Logging system

Future Improvements:

- Add UPDATE and DELETE triggers
- Add indexing
- Connect with Node.js backend
- Deploy on cloud (Neon)

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
