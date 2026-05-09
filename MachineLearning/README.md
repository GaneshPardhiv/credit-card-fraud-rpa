# MachineLearning Folder

## Files

| File | Purpose |
|---|---|
| `model_training.py` | Train the Random Forest fraud detection model |
| `fraud_detection.py` | Main script — run fraud detection on dataset |
| `fraud_model.pkl` | Saved trained model (generated after training) |
| `scaler.pkl` | Saved data scaler (generated after training) |

## How to Run

### Step 1 — Train the Model
```bash
cd MachineLearning
python model_training.py
```
This trains a Random Forest model on the dataset and saves `fraud_model.pkl`.

### Step 2 — Run Fraud Detection
```bash
python fraud_detection.py
```
This loads the model, scans all transactions, and generates a fraud report in `/Reports/`.

## Model Details

| Detail | Value |
|---|---|
| Algorithm | Random Forest Classifier |
| Features Used | 9 engineered features |
| Train/Test Split | 80% / 20% |
| Class Balancing | `class_weight='balanced'` |
| Fraud Threshold | 0.65 probability |

## Features Used by the Model

| Feature | What it Represents |
|---|---|
| `LogAmount` | Log-scaled transaction amount |
| `IsHighAmount` | 1 if amount > ₹50,000 |
| `IsMediumAmount` | 1 if ₹15,000 < amount ≤ ₹50,000 |
| `IsForeignLocation` | 1 if transaction is outside India |
| `IsNight` | 1 if transaction time is 12AM–5AM |
| `DayOfWeek` | 0 (Monday) to 6 (Sunday) |
| `PaymentCode` | Encoded payment method |
| `CategoryRisk` | Risk score based on merchant category |
| `Hour` | Hour of transaction (0–23) |
