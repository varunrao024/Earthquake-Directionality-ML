import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("results/figures").mkdir(parents=True, exist_ok=True)

# Load saved evaluation results
comparison = pd.read_csv("results/model_comparison.csv")
predictions = pd.read_csv("results/model_predictions.csv")

best_model = comparison.iloc[0]["Model"]
actual = predictions["Actual"]
predicted = predictions[best_model]
residuals = actual - predicted

# 1. Model comparison
plt.figure(figsize=(8, 5))
plt.bar(comparison["Model"], comparison["MAE"])
plt.ylabel("Mean Absolute Error")
plt.title("Model Comparison: Grouped Cross-Validation")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("results/figures/model_comparison.png", dpi=300)
plt.close()

# 2. Actual versus predicted
plt.figure(figsize=(6, 6))
plt.scatter(actual, predicted, alpha=0.4)
low = min(actual.min(), predicted.min())
high = max(actual.max(), predicted.max())
plt.plot([low, high], [low, high], linestyle="--")
plt.xlabel("Actual PGA Log Difference")
plt.ylabel("Predicted PGA Log Difference")
plt.title(f"Actual vs Predicted: {best_model}")
plt.tight_layout()
plt.savefig("results/figures/actual_vs_predicted.png", dpi=300)
plt.close()

# 3. Residual distribution
plt.figure(figsize=(7, 5))
plt.hist(residuals, bins=30, edgecolor="black")
plt.axvline(0, linestyle="--")
plt.xlabel("Residual (Actual - Predicted)")
plt.ylabel("Frequency")
plt.title(f"Residual Distribution: {best_model}")
plt.tight_layout()
plt.savefig("results/figures/residual_distribution.png", dpi=300)
plt.close()

print("Saved report figures:")
print("results/figures/model_comparison.png")
print("results/figures/actual_vs_predicted.png")
print("results/figures/residual_distribution.png")