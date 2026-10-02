
# Earthquake Ground Motion Analysis Using Machine Learning

## Project Overview

This project explores earthquake ground-motion characteristics using machine learning and data from the NGA-West2 flatfile. It investigates differences in peak ground acceleration (PGA) between nearby recording stations during the same earthquake.

The project also includes a demonstration of calculating a provisional maximum horizontal acceleration direction from two recorded ground-motion components.

**Note:** Due to limited access to waveform data, this is an exploratory PGA-difference prediction study, not a full reproduction of the original earthquake directionality research.

## Objectives

- Explore and preprocess earthquake ground-motion data from NGA-West2.
- Identify pairs of nearby recording stations for the same earthquake.
- Analyze differences in PGA between paired stations.
- Train and compare machine learning regression models.
- Evaluate model performance using earthquake-grouped cross-validation.
- Visualize model predictions, residuals, and performance.

## Dataset

The project uses the NGA-West2 ground-motion flatfile and a sample Düzce earthquake waveform.

- Flatfile: NGA-West2 RotD50, d005 version.
- Waveform demonstration: Düzce, Turkey, earthquake recorded at station 362.
- Candidate station pairs: 1,667 after filtering.
- Final ML dataset: 1,545 rows across 47 earthquakes.

The waveform demonstration uses two horizontal acceleration components to estimate the direction associated with the maximum rotated PGA. This is a provisional calculation and is not the original paper's complete directionality target.

## Methodology

1. **Data inspection:** Load and examine the NGA-West2 flatfile.
2. **Preprocessing:** Filter records with magnitude greater than 5 and valid station coordinates.
3. **Station pairing:** Identify distinct stations recording the same earthquake within 5 km.
4. **Pair filtering:** Remove pairs with near-zero station separation.
5. **Feature engineering:** Prepare magnitude, inter-station distance, and source-to-site azimuth difference.
6. **Target construction:** Calculate the absolute difference between the stations' log-transformed PGA values.
7. **Model training:** Train and compare a mean baseline, Linear Regression, Ridge Regression, and Random Forest.
8. **Evaluation:** Use 5-fold GroupKFold cross-validation, grouping records by earthquake ID.
9. **Visualization:** Generate model comparison, actual-versus-predicted, and residual distribution plots.

## Machine Learning Models

- Mean Baseline
- Linear Regression
- Ridge Regression
- Random Forest Regressor

## Results

The models were evaluated using mean absolute error (MAE) and the coefficient of determination (R²).

| Model | MAE | R² |
|---|---:|---:|
| Mean Baseline | 0.1070 | -0.0184 |
| Linear Regression | 0.1006 | 0.0490 |
| Ridge Regression | 0.1006 | 0.0491 |
| Random Forest | 0.1045 | 0.0363 |

Ridge Regression achieved the lowest MAE, although its performance was very close to Linear Regression. The relatively low R² values indicate that the selected features explain only a small portion of the variation in PGA differences.

The MAE is measured in absolute log10 PGA-difference units, not degrees or raw acceleration units.

## Visualizations

The generated plots are saved in `results/figures/`.

- `model_comparison.png` — MAE comparison across models.
- `actual_vs_predicted.png` — Actual versus predicted PGA log differences for Ridge Regression.
- `residual_distribution.png` — Distribution of Ridge Regression residuals.

## Project Structure

```text
Earthquake-Directionality-ML/
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   └── best_pga_model.joblib
├── notebooks/
├── results/
│   ├── figures/
│   ├── candidate_station_pairs.csv
│   ├── filtered_station_pairs.csv
│   ├── model_comparison.csv
│   └── model_predictions.csv
├── src/
│   ├── inspect_flatfile.py
│   ├── build_station_pairs.py
│   ├── inspect_pairs.py
│   ├── check_pair_quality.py
│   ├── filter_pairs.py
│   ├── prepare_ml_dataset.py
│   ├── prepare_model_data.py
│   ├── train_models.py
│   ├── visualize_results.py
│   └── calculate_direction.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/Earthquake-Directionality-ML.git
cd Earthquake-Directionality-ML
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the Project

Run the scripts from the project root directory in the following order, after placing the required dataset files in `data/raw/`:

```bash
python src/inspect_flatfile.py
python src/build_station_pairs.py
python src/inspect_pairs.py
python src/check_pair_quality.py
python src/filter_pairs.py
python src/prepare_ml_dataset.py
python src/prepare_model_data.py
python src/train_models.py
python src/visualize_results.py
```

To run the waveform direction demonstration, place the sample AT2 files in `data/raw/` and execute:

```bash
python src/calculate_direction.py
```

## Limitations

- The original research target was the angular difference between maximum ground-motion directions at nearby stations. The complete waveform dataset needed to construct that target was not available for this project.
- The implemented ML target is the absolute difference in log-transformed PGA, which is a different prediction task.
- The model uses a limited set of features and has low explanatory power.
- The sample waveform direction calculation is provisional and does not establish reproduction of the original paper's methodology.
- Results are exploratory and should not be interpreted as a validated earthquake engineering prediction system.

## Technologies Used

- Python
- Pandas and NumPy
- Matplotlib
- Scikit-learn
- SciPy
- Joblib

## References

- NGA-West2 Ground Motion Database: https://ngawest2.berkeley.edu/
- PEER Ground Motion Data Base Reader example repository: https://github.com/GeorgePapazafeiropoulos/PEER-Ground-Motion-Data-Base-Reader

