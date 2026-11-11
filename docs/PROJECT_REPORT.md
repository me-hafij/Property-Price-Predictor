# Project Report: Real Estate Price Predictor

## 1. Abstract
The Real Estate Price Predictor is a Python application designed to estimate the approximate value of a residential property from its area, number of bedrooms and bathrooms, age, floor, parking availability and locality. It applies supervised regression using a Random Forest model and provides a desktop interface for entering property information and viewing predictions.

## 2. Problem statement
Property prices vary with several factors, making manual estimation difficult for a beginner or first-time buyer. This project demonstrates how structured property data and machine learning can be used to produce a consistent indicative estimate.

## 3. Objectives
- Prepare a structured dataset of residential property attributes.
- Train a regression model to estimate property prices.
- Evaluate the model using Mean Absolute Error and R².
- Develop a simple desktop interface.
- Validate user input and export prediction history.

## 4. Tools and technologies
Python, CSV, pandas, scikit-learn, RandomForestRegressor and Tkinter. The GUI uses Python's standard Tkinter library.

## 5. Dataset and features
The included demonstration dataset is synthetic. Each record contains area in square feet, bedrooms, bathrooms, property age in years, floor, parking spaces, location and target price in lakh rupees. Locations include Kolkata, Howrah, Salt Lake, New Town, Bardhaman and Durgapur.

## 6. Methodology
1. Read property records from CSV.
2. Separate input features from target price.
3. Encode the categorical location using one-hot encoding.
4. Split data into training and test subsets.
5. Train a Random Forest regression model.
6. Calculate MAE and R² on held-out test data.
7. Accept user inputs in the GUI and generate an estimate.
8. Store each prediction in the session history and allow CSV export.

## 7. System modules
- Dataset loader: reads and validates CSV data.
- Model trainer: builds a preprocessing and regression pipeline.
- Prediction module: returns the estimated price.
- GUI module: collects input and displays results.
- History/export module: records predictions and writes CSV output.

## 8. Testing
The test suite checks dataset loading, positive price estimates, price formatting, invalid input rejection and prediction behavior. Run the tests with `python -m unittest discover -s tests -v`.

## 9. Limitations
The supplied data is synthetic and cannot represent current market prices accurately. Property valuation also depends on legal title, building condition, amenities, exact street, demand, infrastructure and current market conditions, which are not fully represented in this model.

## 10. Future scope
Use verified real transaction data, add more locality-level features, compare multiple regression algorithms, improve explainability, build a web interface and provide map-based locality selection.

## 11. Conclusion
The project demonstrates an end-to-end machine-learning workflow, from structured data and regression training to GUI-based prediction and result export. It is an educational prototype rather than a certified valuation system.

## Team
Mijanur Rahaman — BWU/BTA/25/596  
Hafizur Rahaman — BWU/BTA/25/594  
Sahil Azad — BWU/BTA/25/574  
Simran Yasmin — BWU/BTA/25/595
