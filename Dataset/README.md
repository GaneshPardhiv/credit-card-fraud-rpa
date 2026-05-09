# Dataset Folder

## File: transactions.csv

This file contains **500 simulated credit card transactions** used for training and testing the fraud detection system.

### Columns Description

| Column | Type | Description |
|---|---|---|
| `Transaction_ID` | String | Unique ID for each transaction (e.g., TXN_00001) |
| `Card_Number` | String | Masked card number (last 4 digits shown) |
| `Cardholder_Name` | String | Name of the cardholder |
| `Timestamp` | DateTime | Date and time of transaction |
| `Amount_INR` | Float | Transaction amount in Indian Rupees |
| `Location` | String | City and country of the transaction |
| `Merchant_Name` | String | Name of the merchant/store |
| `Merchant_Category` | String | Category (Grocery, Electronics, Travel, etc.) |
| `Payment_Method` | String | How payment was made (Swipe, Online, ATM, etc.) |
| `Is_Fraud` | Integer | 0 = Legitimate, 1 = Fraudulent |
| `Fraud_Reason` | String | Why the transaction was flagged (if fraud) |

### Dataset Statistics

- Total Records: 500
- Legitimate Transactions: ~286
- Fraudulent Transactions: ~214
- Date Range: October–November 2025

### Fraud Conditions Applied

1. Amount > ₹50,000 → High Amount flag
2. Location outside India → Foreign Location flag
3. Transaction hour < 5 AM → Unusual Timing flag
4. Unknown/Luxury category + Amount > ₹20,000 → Suspicious Category flag
5. Random 2% chance → ML Model Flag

> **Note:** This is a simulated dataset for academic purposes only. No real customer data is used.
