# 💳 Automated Credit Card Transaction Monitoring using UiPath (RPA)

> Final Year B.Tech CSE Project | Lovely Professional University

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![UiPath](https://img.shields.io/badge/UiPath-Studio-orange.svg)](https://www.uipath.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-green.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)]()

---

## 📌 Project Overview

This project automates the process of **monitoring credit card transactions** and **detecting fraudulent activity** using **UiPath RPA** combined with a **Machine Learning fraud detection model** built in Python.

Instead of manually reviewing thousands of transactions every day, this system:
- Automatically reads transaction data from Excel/CSV
- Runs a trained ML model to predict fraud probability
- Flags suspicious transactions based on rule-based conditions
- Generates a clean fraud report automatically
- Sends alert notifications for high-risk transactions

This reduces human effort significantly and improves detection speed and accuracy.

---

## 👨‍💻 Author Details

| Field | Details |
|---|---|
| **Author** | Ganesh Pardhiv Duvvuri Na |
| **University** | Lovely Professional University (LPU) |
| **Department** | B.Tech Computer Science & Engineering |
| **Guide Faculty** | Mr. Kumar Saurabh |
| **Academic Year** | 2025–2026 |

---

## 🚀 Main Features

- ✅ Reads transaction data from CSV / Excel automatically (via UiPath)
- ✅ Rule-based suspicious transaction detection (amount, location, timing)
- ✅ ML-based fraud probability scoring using Scikit-learn
- ✅ Auto-generates fraud report in Excel/CSV format
- ✅ Alert notification system for high-risk flagged transactions
- ✅ Reduces manual monitoring effort by ~80%
- ✅ Simple and beginner-friendly code structure

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **UiPath Studio** | RPA workflow automation |
| **Python 3.8+** | ML model + data processing |
| **Pandas** | Data loading and manipulation |
| **Scikit-learn** | Fraud detection ML model |
| **NumPy** | Numerical computations |
| **Microsoft Excel** | Input/Output data files |
| **Windows OS** | Platform for UiPath execution |

---

## 📁 Folder Structure

```
credit-card-fraud-rpa/
│
├── 📂 Dataset/
│   ├── transactions.csv          # Sample transaction dataset (500 records)
│   └── README.md                 # Dataset description
│
├── 📂 MachineLearning/
│   ├── fraud_detection.py        # Main fraud detection script
│   ├── model_training.py         # ML model training script
│   └── README.md                 # ML module explanation
│
├── 📂 Workflow/
│   ├── workflow_explanation.md   # Step-by-step UiPath workflow guide
│   └── README.md                 # Workflow overview
│
├── 📂 Reports/
│   ├── sample_fraud_report.csv   # Sample generated fraud report
│   ├── sample_output.txt         # Sample console output log
│   └── README.md                 # Reports explanation
│
├── 📂 Screenshots/
│   └── README.md                 # Screenshot placeholders and guide
│
├── README.md                     # Main project documentation (this file)
├── requirements.txt              # Python dependencies
├── .gitignore                    # Files to ignore in Git
├── LICENSE                       # MIT License
└── project_description.md        # Short GitHub project description
```

---

## ⚙️ Fraud Detection Conditions

The system flags a transaction as suspicious if any of the following are true:

| Condition | Rule |
|---|---|
| **High Amount** | Transaction > ₹50,000 in a single step |
| **Foreign Location** | Transaction from outside registered country |
| **Unusual Timing** | Transactions between 12 AM – 5 AM |
| **Multiple Rapid Transactions** | 3+ transactions within 10 minutes |
| **ML Fraud Score** | Model probability > 70% |

---

## 📊 How It Works (Simple Explanation)

```
[Step 1] UiPath reads transactions.csv from the Dataset folder
         ↓
[Step 2] Data is passed to the Python ML script
         ↓
[Step 3] Python checks each transaction against fraud rules
         ↓
[Step 4] ML model gives a fraud probability score (0 to 1)
         ↓
[Step 5] Transactions above threshold are flagged as FRAUD
         ↓
[Step 6] UiPath writes results into a fraud_report.csv
         ↓
[Step 7] Alert notification is triggered for flagged records
```

---

## 🧰 Installation & Setup

### Step 1 – Clone the Repository
```bash
git clone https://github.com/ganesh-pardhiv/credit-card-fraud-rpa.git
cd credit-card-fraud-rpa
```

### Step 2 – Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 – Run the ML Fraud Detection Script
```bash
cd MachineLearning
python fraud_detection.py
```

### Step 4 – Open UiPath Workflow
1. Open **UiPath Studio**
2. Open the `.xaml` workflow file from the `/Workflow` folder
3. Set the dataset path to `/Dataset/transactions.csv`
4. Click **Run** to execute the automation

### Step 5 – Check Output
- Fraud report will be saved in `/Reports/fraud_report.csv`
- Console log will show flagged transactions

---

## 📈 Sample Output

```
========================================
  FRAUD DETECTION SYSTEM - RUN REPORT
========================================
Total Transactions Scanned : 500
Legitimate Transactions    : 463
Flagged as Suspicious      : 37
Fraud Probability (Avg)    : 0.82
Report Generated At        : 2025-11-15 14:32:10
========================================

[ALERT] Transaction ID: TXN_00342 → FRAUD DETECTED
  Amount     : ₹1,25,000
  Location   : Dubai, UAE
  Time       : 03:14 AM
  Reason     : High amount + Foreign location + Unusual timing
```

---

## 🔮 Future Scope

1. **Real-time API Integration** – Connect directly to bank APIs for live transaction monitoring
2. **Deep Learning Model** – Replace Logistic Regression with LSTM for sequence-based fraud patterns
3. **Email/SMS Alerts** – Integrate Twilio or SendGrid for real-time alert delivery
4. **Web Dashboard** – Build a Streamlit dashboard to visualize fraud statistics
5. **Cloud Deployment** – Host the ML model on AWS or Azure for scalable access
6. **Multi-language Support** – Extend to support international transaction formats
7. **Mobile App Alerts** – Push notifications to cardholder mobile app

---

## 📸 Screenshots

> Screenshots of UiPath workflow, model output, and generated reports are available in the `/Screenshots` folder.

| Screenshot | Description |
|---|---|
| `uipath_workflow.png` | UiPath Studio workflow design |
| `fraud_report_output.png` | Sample generated fraud report |
| `ml_model_accuracy.png` | Confusion matrix and accuracy graph |
| `alert_notification.png` | Sample alert message triggered |

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **Mr. Kumar Saurabh** – Faculty Guide, LPU
- **Lovely Professional University** – For academic support
- UiPath Community Documentation
- Scikit-learn open-source library contributors
- Kaggle Credit Card Fraud Dataset (inspiration)

---

> ⭐ If you found this project useful, give it a star on GitHub!
