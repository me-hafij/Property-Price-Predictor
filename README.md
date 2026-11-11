# Real Estate Price Predictor — Group 9

A Python desktop application that estimates residential property prices using property attributes and location. The project demonstrates data preparation, supervised machine learning, model evaluation, a Tkinter interface and CSV export.

## Team
- Mijanur Rahaman — BWU/BTA/25/596
- Hafizur Rahaman — BWU/BTA/25/594
- Sahil Azad — BWU/BTA/25/574
- Simran Yasmin — BWU/BTA/25/595

## Academic details
Brainware University · BTECH-CSE(AIML)2026 · Semester 3 · Section J  
Course: Python for Machine Learning · Course code: BTA30104

## Run on Windows
1. Install Python 3.10 or newer.
2. Open this folder in Command Prompt or PowerShell.
3. Install dependencies: `py -3 -m pip install -r requirements.txt`
4. Start the desktop app: `py -3 gui.py`
5. Or double-click `run_gui.bat`.

For the terminal demonstration run `py -3 main.py` or `run_demo.bat`.

## Project structure
- `main.py`: data loading, model training, evaluation and prediction.
- `gui.py`: desktop GUI, validation, prediction history and CSV export.
- `examples/real_estate_data.csv`: included illustrative dataset.
- `tests/`: automated tests.
- `docs/PROJECT_REPORT.md`: technical project report.

## Model
The primary model is a Random Forest regression pipeline. Location is one-hot encoded and numeric features are passed through. The data is split into training and test sets. MAE and R² are displayed by the terminal demonstration. If scikit-learn is unavailable, a transparent rule-based estimate is used so the application can still be demonstrated.

## Important limitation
The included dataset is synthetic and intended for academic demonstration. Predictions are not professional valuations, loan assessments or investment advice. For real-world use, replace it with verified, current transaction data and retrain/evaluate the model.

## Testing
Run: `py -3 -m unittest discover -s tests -v`
