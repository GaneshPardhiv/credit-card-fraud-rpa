# UiPath Workflow Explanation

## Project: Automated Credit Card Transaction Monitoring

**File:** `Main.xaml` (open in UiPath Studio)

---

## Overview

The UiPath workflow acts as the **automation backbone** of this project. It handles all file reading, invoking the Python script, reading the output, and generating alerts — without any human involvement.

---

## Workflow Steps (UiPath Activities Used)

### SEQUENCE 1 — Initialize

| Step | UiPath Activity | What It Does |
|---|---|---|
| 1 | `Log Message` | Logs "Workflow Started" to console |
| 2 | `Assign` | Sets file paths for input CSV and output report |
| 3 | `File Exists` | Checks if transactions.csv exists before proceeding |

---

### SEQUENCE 2 — Read Transaction Data

| Step | UiPath Activity | What It Does |
|---|---|---|
| 4 | `Read CSV` | Reads `Dataset/transactions.csv` into a DataTable |
| 5 | `Log Message` | Logs total row count loaded |
| 6 | `Assign` | Stores total transaction count in variable |

---

### SEQUENCE 3 — Invoke Python Script

| Step | UiPath Activity | What It Does |
|---|---|---|
| 7 | `Invoke Python Script` | Runs `MachineLearning/fraud_detection.py` |
| 8 | `Get Python Object` | Retrieves fraud probability results |
| 9 | `Log Message` | Logs "ML script completed" |

---

### SEQUENCE 4 — Read Fraud Report Output

| Step | UiPath Activity | What It Does |
|---|---|---|
| 10 | `Read CSV` | Reads the generated `fraud_report.csv` |
| 11 | `Filter Data Table` | Filters rows where AlertLevel = CRITICAL or HIGH |
| 12 | `For Each Row` | Loops through each flagged transaction |

---

### SEQUENCE 5 — Alert Generation

| Step | UiPath Activity | What It Does |
|---|---|---|
| 13 | `If Condition` | Checks if FinalVerdict = "FRAUD" |
| 14 | `Write Line` | Prints alert details to UiPath console |
| 15 | `Send Outlook Mail Message` *(optional)* | Sends email alert to fraud team |
| 16 | `Append Line` | Appends alert log to output log file |

---

### SEQUENCE 6 — Generate Final Report

| Step | UiPath Activity | What It Does |
|---|---|---|
| 17 | `Write CSV` | Writes filtered fraud records to final report |
| 18 | `Write Cell` *(Excel)* | Updates summary stats in Excel sheet |
| 19 | `Log Message` | Logs "Report Generated Successfully" |
| 20 | `Message Box` | Shows popup: "Fraud Detection Complete" |

---

## Variables Used in Workflow

| Variable | Type | Description |
|---|---|---|
| `dtTransactions` | DataTable | All 500 transaction records |
| `dtFraudReport` | DataTable | Filtered fraud-only records |
| `strDatasetPath` | String | Path to transactions.csv |
| `strReportPath` | String | Path to output fraud_report.csv |
| `intTotalRows` | Integer | Total transactions scanned |
| `intFraudCount` | Integer | Total fraud transactions found |
| `strTimestamp` | String | Current run datetime |

---

## UiPath Packages Required

Install these from UiPath Package Manager:

- `UiPath.Excel.Activities` — For Excel read/write
- `UiPath.CSV.Activities` — For CSV operations
- `UiPath.Python.Activities` — For running Python script
- `UiPath.Mail.Activities` — For sending alert emails *(optional)*
- `UiPath.System.Activities` — Core activities (File, Log, etc.)

---

## How to Run in UiPath Studio

1. Open **UiPath Studio**
2. Open `Workflow/Main.xaml`
3. Go to **Manage Packages** and install required packages
4. Set variable `strDatasetPath` = path to your `transactions.csv`
5. Click **Run** (F5) or **Debug** to execute
6. Check `/Reports/fraud_report.csv` for output

---

> **Note:** The Python environment must be set up with required packages before running the UiPath workflow. Run `pip install -r requirements.txt` first.
