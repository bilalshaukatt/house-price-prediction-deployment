
# House Price Category Predictor

A Streamlit web application that predicts whether a house is likely to be
**Expensive** or **Affordable** (relative to the dataset median), based on
key property features. Built on the Ames Housing dataset as the final
deployment task for the Auspify Technologies Python internship.

## Project Overview

- **Type**: Binary classification web app
- **Model**: Random Forest Classifier (scikit-learn), wrapped in a full
  preprocessing + prediction pipeline
- **Target**: `PriceCategory` — 1 if `SalePrice` is above the dataset
  median ($163,000), else 0
- **Test accuracy**: ~90.75%

## Dataset Description

- Source: Ames Housing dataset (`Week_3_FINAL_CLEANED.csv`), 1,458 rows,
  81 original columns
- For usability, the web form exposes a compact set of the most
  influential features rather than all 80:
  - **Numeric**: OverallQual, GrLivArea, GarageCars, TotalBsmtSF,
    FullBath, YearBuilt, YearRemodAdd, LotArea, Fireplaces
  - **Categorical**: Neighborhood, HouseStyle, ExterQual, KitchenQual
- Note: several categorical columns (e.g. `Alley`, `PoolQC`) use the
  literal string `"None"` to mean "does not have this feature." The
  training script reads the CSV with `keep_default_na=False` so these
  aren't mistaken for missing data.

## Model Description

- **Pipeline**: `ColumnTransformer` (median imputation + scaling for
  numeric features; most-frequent imputation + one-hot encoding for
  categorical features) → `RandomForestClassifier`
  (`n_estimators=200`, `max_depth=10`, `min_samples_split=5`)
- The entire pipeline (preprocessing + model) is saved as a single
  `.pkl` file with `joblib`, so the app never has to guess at
  preprocessing steps at inference time.
- Metadata (feature lists, valid categorical options, numeric ranges,
  median price, test accuracy) is saved separately in
  `model_metadata.pkl` and used to build the form dynamically.

## Requirements

See `requirements.txt`:
```
streamlit>=1.30
scikit-learn>=1.6
pandas
joblib
numpy
plotly>=5.18
```

## Installation Instructions

```bash
git clone <your-repo-url>
cd <repo-folder>
pip install -r requirements.txt
```

## Interface

The app has three tabs:
- **🔮 Predict** — the input form, a live prediction result banner, and a
  Plotly confidence gauge
- **📊 Model Insights** — an interactive feature-importance chart showing
  what drives the model's decisions
- **📜 History** — a log of every prediction made this session, quick
  stats, a confidence trend line chart, and CSV export

It uses a custom gradient theme, card-style layout, and a dark mode toggle
(sidebar).

Run locally:
```bash
streamlit run app.py
```
Then open the URL shown in the terminal (typically `http://localhost:8501`).

**In the app:**
1. Fill in the property details in the form (quality, size, neighborhood, etc.)
2. Click **Predict**
3. View the predicted category (Expensive / Affordable) and the model's
   confidence score
4. Click **Reset** to clear the form and start a new prediction
5. Every prediction is logged in the **Prediction History** table below
   the form, which can be downloaded as a CSV

## Deployment

### Streamlit Community Cloud (recommended)
1. Push this folder to a public GitHub repository (must include
   `app.py`, `house_price_model.pkl`, `model_metadata.pkl`,
   `requirements.txt`)
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with
   GitHub
3. Click **New app**, select your repo/branch, set the main file path
   to `app.py`
4. Click **Deploy** — you'll get a public URL like
   `https://<your-app>.streamlit.app`

### Alternative: Render / Railway
Both platforms can run this as a web service using:
```
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

## Deployment URL
_Add your live Streamlit Community Cloud URL here after deploying._

## GitHub Repository
_Add your repository link here after pushing the code._

## Screenshots
_Add screenshots of the running app here (form, prediction result, and
prediction history) — see PROJECT_REPORT.md for exact instructions._

## Bonus Features Implemented
- ✅ Prediction history table (session-based)
- ✅ Download predictions as CSV
- ✅ Dark mode toggle (sidebar)
- ✅ Interactive charts — feature importance (expander) and confidence
  trend across predictions (line chart)
- ✅ Docker containerization (`Dockerfile`, `.dockerignore`)
- ✅ GitHub Actions CI/CD (`.github/workflows/ci.yml`) — installs deps,
  compiles code, retrains the model, runs a prediction smoke test, and
  builds the Docker image on every push/PR
- ✅ Confidence score with progress bar
- ✅ Sidebar with project info, metrics, and instructions
- ✅ Input validation with clear error messages

## Running with Docker
```bash
docker build -t house-price-predictor .
docker run -p 8501:8501 house-price-predictor
```
Then open `http://localhost:8501`.


