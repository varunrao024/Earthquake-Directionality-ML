
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load the prepared dataset
DATA_FILE = "data/processed/model_dataset.csv"
RESULTS_DIR = Path("results")
MODELS_DIR = Path("models")

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

features = [
    "Magnitude",
    "Distance_km",
    "Azimuth_Difference_deg"
]
target = "PGA_Log_Difference"
X = df[features]
y = df[target]
groups = df["EQID"]

# Keep all records from each earthquake in the same validation fold
cv = GroupKFold(n_splits=5)

models = {
    "Mean baseline": DummyRegressor(strategy="mean"),
    "Linear Regression": LinearRegression(),
    "Ridge Regression": make_pipeline(
        StandardScaler(),
        Ridge(alpha=1.0)
    ),
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        max_depth=5,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )
}

results = []
predictions = pd.DataFrame({
    "EQID": groups,
    "Actual": y
})

print("Training and evaluating models with 5-fold grouped CV...")
print("Validation groups: earthquake EQID")
print()

for name, model in models.items():
    predicted = cross_val_predict(
        model,
        X,
        y,
        groups=groups,
        cv=cv,
        n_jobs=-1
    )

    mae = mean_absolute_error(y, predicted)
    r2 = r2_score(y, predicted)

    results.append({
        "Model": name,
        "MAE": mae,
        "R2": r2
    })
    predictions[name] = predicted

    print(f"{name}")
    print(f"  MAE: {mae:.4f}")
    print(f"  R2:  {r2:.4f}")
    print()

# Save evaluation results and out-of-fold predictions
results_df = pd.DataFrame(results).sort_values("MAE")
results_df.to_csv(RESULTS_DIR / "model_comparison.csv", index=False)
predictions.to_csv(RESULTS_DIR / "model_predictions.csv", index=False)

# Fit the lowest-MAE model on the full dataset for the demo
best_name = results_df.iloc[0]["Model"]
best_model = models[best_name]
best_model.fit(X, y)
joblib.dump(best_model, MODELS_DIR / "best_pga_model.joblib")

print("Model comparison:")
print(results_df.to_string(index=False))
print()
print(f"Lowest-CV-MAE model: {best_name}")
print("Saved results/model_comparison.csv")
print("Saved results/model_predictions.csv")
print("Saved models/best_pga_model.joblib")
