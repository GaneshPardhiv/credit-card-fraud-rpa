"""
========================================================
 Automated Credit Card Transaction Monitoring System
 Model Training Script
========================================================
 Author  : Ganesh Pardhiv Duvvuri Na
 Guide   : Mr. Kumar Saurabh
 College : Lovely Professional University (LPU)
 Year    : 2025-2026

 Run this script FIRST before fraud_detection.py
 This trains the ML model and saves it as fraud_model.pkl
========================================================
"""

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, roc_auc_score
)
from sklearn.preprocessing import StandardScaler


# ─────────────────────────────────────────
# LOAD AND PREPARE DATA
# ─────────────────────────────────────────
def prepare_training_data(path="../Dataset/transactions.csv"):
    print("[INFO] Loading dataset for training...")
    df = pd.read_csv(path)

    df["Timestamp"]          = pd.to_datetime(df["Timestamp"])
    df["Hour"]               = df["Timestamp"].dt.hour
    df["DayOfWeek"]          = df["Timestamp"].dt.dayofweek
    df["IsNight"]            = ((df["Hour"] >= 0) & (df["Hour"] < 5)).astype(int)
    df["IsForeignLocation"]  = (~df["Location"].str.contains("India", na=False)).astype(int)
    df["IsHighAmount"]       = (df["Amount_INR"] > 50000).astype(int)
    df["IsMediumAmount"]     = ((df["Amount_INR"] > 15000) & (df["Amount_INR"] <= 50000)).astype(int)
    df["LogAmount"]          = np.log1p(df["Amount_INR"])

    pay_map = {"Swipe": 0, "Online": 1, "Contactless": 2, "ATM": 3, "International": 4}
    df["PaymentCode"] = df["Payment_Method"].map(pay_map).fillna(5)

    risky = {"Unknown": 3, "Luxury Goods": 2, "Travel": 1, "ATM Withdrawal": 1}
    df["CategoryRisk"] = df["Merchant_Category"].map(risky).fillna(0)

    print(f"[INFO] Dataset shape: {df.shape}")
    print(f"[INFO] Fraud distribution:\n{df['Is_Fraud'].value_counts()}")
    return df


# ─────────────────────────────────────────
# TRAIN MODEL
# ─────────────────────────────────────────
def train_model(df):
    feature_cols = [
        "LogAmount", "IsHighAmount", "IsMediumAmount",
        "IsForeignLocation", "IsNight", "DayOfWeek",
        "PaymentCode", "CategoryRisk", "Hour"
    ]

    X = df[feature_cols]
    y = df["Is_Fraud"]

    # Split: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\n[INFO] Train size : {len(X_train)}")
    print(f"[INFO] Test  size : {len(X_test)}")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # Train Random Forest (works well for imbalanced fraud data)
    print("\n[INFO] Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42,
        class_weight="balanced"   # handles imbalanced fraud/legit ratio
    )
    model.fit(X_train_scaled, y_train)

    # Evaluate
    y_pred      = model.predict(X_test_scaled)
    y_prob      = model.predict_proba(X_test_scaled)[:, 1]
    accuracy    = accuracy_score(y_test, y_pred)
    roc_auc     = roc_auc_score(y_test, y_prob)

    print("\n" + "=" * 50)
    print("  MODEL EVALUATION RESULTS")
    print("=" * 50)
    print(f"  Accuracy   : {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"  ROC-AUC    : {roc_auc:.4f}")
    print("\n  Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Legit", "Fraud"]))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("  Confusion Matrix:")
    print(f"    TN={cm[0][0]}  FP={cm[0][1]}")
    print(f"    FN={cm[1][0]}  TP={cm[1][1]}")
    print("=" * 50)

    return model, scaler, X_test_scaled, y_test, feature_cols


# ─────────────────────────────────────────
# SAVE MODEL
# ─────────────────────────────────────────
def save_model(model, scaler):
    joblib.dump(model,  "fraud_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    print("\n[INFO] Model saved as fraud_model.pkl")
    print("[INFO] Scaler saved as scaler.pkl")
    print("[INFO] You can now run fraud_detection.py")


# ─────────────────────────────────────────
# FEATURE IMPORTANCE PLOT
# ─────────────────────────────────────────
def plot_feature_importance(model, feature_cols):
    importance = pd.Series(model.feature_importances_, index=feature_cols)
    importance = importance.sort_values(ascending=True)

    plt.figure(figsize=(8, 5))
    importance.plot(kind="barh", color="steelblue")
    plt.title("Feature Importance — Fraud Detection Model", fontsize=13)
    plt.xlabel("Importance Score")
    plt.tight_layout()
    plt.savefig("../Screenshots/feature_importance.png", dpi=150)
    print("[INFO] Feature importance chart saved to Screenshots/")


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  ML Model Training — Credit Card Fraud Detection")
    print("  Author: Ganesh Pardhiv Duvvuri Na | LPU 2026")
    print("=" * 50)

    df                              = prepare_training_data()
    model, scaler, X_test, y_test, feature_cols = train_model(df)
    save_model(model, scaler)

    # Optional: plot feature importance
    try:
        plot_feature_importance(model, feature_cols)
    except Exception as e:
        print(f"[WARN] Could not save plot: {e}")

    print("\n[DONE] Training complete. Ready for fraud_detection.py")
