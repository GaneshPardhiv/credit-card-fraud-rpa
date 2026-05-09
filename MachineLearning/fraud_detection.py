"""
========================================================
 Automated Credit Card Transaction Monitoring System
 Fraud Detection Module - Main Script
========================================================
 Author  : Ganesh Pardhiv Duvvuri Na
 Guide   : Mr. Kumar Saurabh
 College : Lovely Professional University (LPU)
 Year    : 2025-2026
========================================================
"""

import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime

# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────
DATASET_PATH = "../Dataset/transactions.csv"
MODEL_PATH   = "fraud_model.pkl"
REPORT_PATH  = "../Reports/fraud_report.csv"
THRESHOLD    = 0.65   # ML fraud probability threshold


# ─────────────────────────────────────────
# STEP 1: LOAD DATASET
# ─────────────────────────────────────────
def load_data(path):
    """Load transaction CSV file into a DataFrame."""
    print("\n[INFO] Loading transaction data...")
    df = pd.read_csv(path)
    print(f"[INFO] Loaded {len(df)} transactions successfully.")
    return df


# ─────────────────────────────────────────
# STEP 2: FEATURE ENGINEERING
# ─────────────────────────────────────────
def engineer_features(df):
    """
    Create features the ML model uses for prediction.
    We convert raw columns into numbers the model understands.
    """
    print("\n[INFO] Engineering features...")

    df = df.copy()

    # Parse timestamp
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Hour"]       = df["Timestamp"].dt.hour
    df["DayOfWeek"]  = df["Timestamp"].dt.dayofweek   # 0=Mon, 6=Sun
    df["IsNight"]    = ((df["Hour"] >= 0) & (df["Hour"] < 5)).astype(int)

    # Is location in India?
    df["IsForeignLocation"] = (~df["Location"].str.contains("India", na=False)).astype(int)

    # Amount flags
    df["IsHighAmount"]       = (df["Amount_INR"] > 50000).astype(int)
    df["IsMediumAmount"]     = ((df["Amount_INR"] > 15000) & (df["Amount_INR"] <= 50000)).astype(int)
    df["LogAmount"]          = np.log1p(df["Amount_INR"])

    # Payment method encoding
    pay_map = {"Swipe": 0, "Online": 1, "Contactless": 2, "ATM": 3, "International": 4}
    df["PaymentCode"] = df["Payment_Method"].map(pay_map).fillna(5)

    # Category risk score
    risky_categories = {"Unknown": 3, "Luxury Goods": 2, "Travel": 1, "ATM Withdrawal": 1}
    df["CategoryRisk"] = df["Merchant_Category"].map(risky_categories).fillna(0)

    print("[INFO] Feature engineering complete.")
    return df


# ─────────────────────────────────────────
# STEP 3: RULE-BASED FRAUD FLAGS
# ─────────────────────────────────────────
def apply_rules(df):
    """
    Flag transactions based on simple business rules.
    These rules run even without the ML model.
    """
    print("\n[INFO] Applying rule-based fraud detection...")

    df = df.copy()
    df["RuleFlag"] = 0
    df["RuleReason"] = ""

    for idx, row in df.iterrows():
        reasons = []

        if row["Amount_INR"] > 50000:
            reasons.append("High Amount (>50K)")

        if "India" not in str(row["Location"]):
            reasons.append("Foreign Location")

        hour = row["Timestamp"].hour if hasattr(row["Timestamp"], "hour") else 12
        if hour < 5:
            reasons.append("Unusual Timing (12AM-5AM)")

        if row["Merchant_Category"] in ["Unknown", "Luxury Goods"] and row["Amount_INR"] > 20000:
            reasons.append("Suspicious Category + High Amount")

        if reasons:
            df.at[idx, "RuleFlag"] = 1
            df.at[idx, "RuleReason"] = " | ".join(reasons)

    flagged = df["RuleFlag"].sum()
    print(f"[INFO] Rule-based flags: {flagged} transactions flagged.")
    return df


# ─────────────────────────────────────────
# STEP 4: ML MODEL PREDICTION
# ─────────────────────────────────────────
def predict_fraud(df, model_path):
    """
    Use the trained ML model to predict fraud probability.
    If no model file found, skip ML step and use rules only.
    """
    feature_cols = [
        "LogAmount", "IsHighAmount", "IsMediumAmount",
        "IsForeignLocation", "IsNight", "DayOfWeek",
        "PaymentCode", "CategoryRisk", "Hour"
    ]

    if os.path.exists(model_path):
        print(f"\n[INFO] Loading ML model from {model_path}...")
        model = joblib.load(model_path)
        X = df[feature_cols]
        df["FraudProbability"] = model.predict_proba(X)[:, 1]
        df["MLFlag"] = (df["FraudProbability"] >= THRESHOLD).astype(int)
        print(f"[INFO] ML prediction done. Avg fraud probability: {df['FraudProbability'].mean():.3f}")
    else:
        print("\n[WARN] No trained model found. Run model_training.py first.")
        print("[INFO] Using rule-based detection only...")
        df["FraudProbability"] = df["RuleFlag"].astype(float)
        df["MLFlag"] = df["RuleFlag"]

    return df


# ─────────────────────────────────────────
# STEP 5: COMBINE FLAGS & FINAL VERDICT
# ─────────────────────────────────────────
def finalize_verdict(df):
    """
    Combine rule-based flag and ML flag to give final fraud verdict.
    A transaction is FRAUD if either the rules OR the ML model flag it.
    """
    df["FinalVerdict"] = np.where(
        (df["RuleFlag"] == 1) | (df["MLFlag"] == 1),
        "FRAUD",
        "LEGITIMATE"
    )
    df["AlertLevel"] = np.where(
        df["FraudProbability"] >= 0.85, "CRITICAL",
        np.where(df["FraudProbability"] >= 0.65, "HIGH",
        np.where(df["FraudProbability"] >= 0.40, "MEDIUM", "LOW"))
    )
    return df


# ─────────────────────────────────────────
# STEP 6: GENERATE FRAUD REPORT
# ─────────────────────────────────────────
def generate_report(df, report_path):
    """
    Save only flagged (FRAUD) transactions into the output report CSV.
    This report is what UiPath reads to send alerts.
    """
    print("\n[INFO] Generating fraud report...")

    fraud_df = df[df["FinalVerdict"] == "FRAUD"].copy()

    report_cols = [
        "Transaction_ID", "Cardholder_Name", "Card_Number",
        "Timestamp", "Amount_INR", "Location",
        "Merchant_Name", "Merchant_Category",
        "FraudProbability", "AlertLevel",
        "RuleReason", "FinalVerdict"
    ]

    report_df = fraud_df[report_cols].copy()
    report_df["FraudProbability"] = report_df["FraudProbability"].round(4)
    report_df = report_df.sort_values("FraudProbability", ascending=False)

    report_df.to_csv(report_path, index=False)
    print(f"[INFO] Report saved to: {report_path}")
    return report_df


# ─────────────────────────────────────────
# STEP 7: PRINT SUMMARY TO CONSOLE
# ─────────────────────────────────────────
def print_summary(df, report_df):
    """Print a clean summary of the fraud detection run."""
    total       = len(df)
    fraud_count = len(report_df)
    legit_count = total - fraud_count
    critical    = len(report_df[report_df["AlertLevel"] == "CRITICAL"])
    high        = len(report_df[report_df["AlertLevel"] == "HIGH"])

    print("\n")
    print("=" * 55)
    print("   FRAUD DETECTION SYSTEM — RUN SUMMARY")
    print("=" * 55)
    print(f"  Run Time                : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Total Transactions      : {total}")
    print(f"  Legitimate              : {legit_count}")
    print(f"  Flagged as FRAUD        : {fraud_count}")
    print(f"  ─ CRITICAL Alerts       : {critical}")
    print(f"  ─ HIGH Alerts           : {high}")
    print("=" * 55)

    print("\n[ALERT PREVIEW] Top 5 High-Risk Transactions:")
    print("-" * 55)
    top5 = report_df.head(5)
    for _, row in top5.iterrows():
        print(f"  {row['Transaction_ID']}  |  ₹{row['Amount_INR']:>10,.2f}  |  {row['AlertLevel']}")
        print(f"    → {row['Location']} | {row['Cardholder_Name']}")
        print(f"    → Reason: {row['RuleReason']}")
        print()

    print("[INFO] Full report saved. UiPath can now process the output.")
    print("=" * 55)


# ─────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  Automated Credit Card Fraud Detection System")
    print("  Author: Ganesh Pardhiv Duvvuri Na | LPU 2026")
    print("=" * 55)

    # Run full pipeline
    df         = load_data(DATASET_PATH)
    df         = engineer_features(df)
    df         = apply_rules(df)
    df         = predict_fraud(df, MODEL_PATH)
    df         = finalize_verdict(df)
    report_df  = generate_report(df, REPORT_PATH)

    print_summary(df, report_df)
