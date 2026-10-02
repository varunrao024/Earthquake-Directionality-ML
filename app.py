
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Earthquake ML Results",
    layout="wide"
)

ROOT = Path(__file__).resolve().parent
FIGURES = ROOT / "results" / "figures"

st.title("Earthquake Ground Motion Prediction")
st.write(
    "An exploratory machine learning study predicting differences "
    "in peak ground acceleration (PGA) between nearby stations."
)

st.divider()

# 1. Model Comparison
st.subheader("1. Model Comparison")
st.image(
    str(FIGURES / "model_comparison.png"),
    use_container_width=True
)
st.write(
    "Ridge Regression achieved the lowest MAE, closely followed by "
    "Linear Regression. Random Forest performed slightly worse, while "
    "the mean baseline had the highest error. Overall, the models "
    "showed only modest improvement over the baseline."
)

st.divider()

# 2. Actual vs Predicted
st.subheader("2. Actual vs. Predicted")
st.image(
    str(FIGURES / "actual_vs_predicted.png"),
    use_container_width=True
)
st.write(
    "The dashed diagonal represents perfect predictions. Points "
    "closer to this line indicate more accurate predictions. The "
    "spread of points, particularly at higher actual values, shows "
    "that the model struggles to predict larger PGA differences."
)

st.divider()

# 3. Residual Distribution
st.subheader("3. Residual Distribution")
st.image(
    str(FIGURES / "residual_distribution.png"),
    use_container_width=True
)
st.write(
    "Residuals are the actual values minus the predicted values. "
    "Positive residuals indicate underprediction, while negative "
    "residuals indicate overprediction. The distribution shows "
    "that errors vary, with some larger underpredictions."
)

st.divider()

st.caption(
    "Note: This project predicts absolute differences in log-transformed "
    "PGA, not the angular difference in maximum ground-motion direction "
    "studied in the original paper. Ridge Regression achieved an R² "
    "of approximately 0.049, indicating limited explanatory power."
)
