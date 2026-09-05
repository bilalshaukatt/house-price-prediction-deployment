# Project Report: Machine Learning Model Deployment (Task 6)

## 1. Objective
Deploy a trained machine learning model as an interactive web application
that accepts user input and returns predictions, satisfying the Auspify
Technologies internship's final deliverable.

## 2. Workflow Summary
```
User Input (form) → Data Pre-processing (impute + scale + one-hot encode)
→ Random Forest Model → Prediction (0/1) + Confidence → Displayed Result
```

## 3. Dataset
The Ames Housing dataset (`Week_3_FINAL_CLEANED.csv`) — 1,458 records,
81 columns describing residential properties in Ames, Iowa, along with
their final `SalePrice`.

A binary target, `PriceCategory`, was engineered from `SalePrice`:
- `1` (Expensive) if `SalePrice` > median ($163,000)
- `0` (Affordable) otherwise

This reframes the original regression problem as a classification
problem so the model can output a class + confidence score, matching
the task's UI requirements (prediction + confidence score).

## 4. Feature Selection
Of the 80 raw features, 13 were selected for the input form based on
their known strong correlation with sale price in the Ames dataset,
balanced against keeping the form usable for a human filling it out
by hand:

| Type | Features |
|---|---|
| Numeric | OverallQual, GrLivArea, GarageCars, TotalBsmtSF, FullBath, YearBuilt, YearRemodAdd, LotArea, Fireplaces |
| Categorical | Neighborhood, HouseStyle, ExterQual, KitchenQual |

## 5. Model Development
- **Algorithm**: Random Forest Classifier
- **Preprocessing**: `ColumnTransformer` combining median imputation +
  standard scaling (numeric) and most-frequent imputation + one-hot
  encoding (categorical), fitted inside the same `Pipeline` as the
  classifier
- **Split**: 80/20 train/test, stratified by target
- **Hyperparameters**: `n_estimators=200`, `max_depth=10`,
  `min_samples_split=5`, `random_state=42`

### Note on the originally provided model file
An earlier trained model (`final_optimized_random_forest.pkl`) was
provided for this task, but it could not be safely deployed: it
expected 300 input features with no record of which preprocessing
steps (encoding, scaling) produced them, and no `feature_names_in_`
metadata was saved alongside it. Deploying it as-is risked silently
mismatched inputs and unreliable predictions. Instead, a new pipeline
was trained directly from the provided CSV with the full preprocessing
logic bundled into the same saved artifact, so the deployed app's
predictions are guaranteed to be consistent with how the model was
trained.

## 6. Results
- **Test accuracy**: 90.75%
- **Precision/Recall**: 0.88–0.93 across both classes (see training
  log / classification report)

## 7. Application Features
- Clean two-column input form with sliders and number inputs for
  numeric fields, dropdowns for categorical fields
- Real-time input validation (e.g. remodel year can't precede build
  year, areas must be positive)
- Prediction button producing a labeled result (Expensive/Affordable)
  with a confidence percentage and progress bar
- Reset button to clear the form
- Sidebar with project description, live model metrics, and usage
  instructions
- Prediction history table (bonus) with CSV export (bonus)
- Dark mode toggle (bonus) — sidebar switch injects a dark CSS theme
- Interactive charts (bonus) — feature importance bar chart (from the
  trained Random Forest) and a confidence-trend line chart across the
  session's predictions
- Docker containerization (bonus) — `Dockerfile` + `.dockerignore` for
  a portable, reproducible deployment
- GitHub Actions CI/CD (bonus) — `.github/workflows/ci.yml` runs on
  every push/PR: installs dependencies, compiles the code, retrains
  the model to catch data/pipeline regressions, runs a prediction
  smoke test, and builds the Docker image

## 8. How to Reproduce
1. `pip install -r requirements.txt`
2. `python train_model.py` (regenerates `house_price_model.pkl` and
   `model_metadata.pkl` from the CSV)
3. `streamlit run app.py`

## 9. Taking Screenshots for Submission
Once running locally (`streamlit run app.py`):
1. Take a screenshot of the empty form (project overview)
2. Fill in sample values, click **Predict**, screenshot the result +
   confidence score
3. Make a couple of predictions, screenshot the **Prediction History**
   table
4. Save these into a `screenshots/` folder and reference them in
   `README.md`

## 10. Deploying with Docker
```bash
docker build -t house-price-predictor .
docker run -p 8501:8501 house-price-predictor
```
This is also validated automatically by the CI pipeline on every push.

## 11. Deliverables Checklist
- [x] Complete source code (`app.py`, `train_model.py`)
- [x] Trained model (`house_price_model.pkl`, `model_metadata.pkl`)
- [x] Working web application (Streamlit)
- [ ] Live deployment URL (deploy via Streamlit Community Cloud — see README)
- [x] README.md
- [x] Project report (this document)
- [ ] GitHub repository (push this folder to GitHub)
- [ ] Application screenshots (capture after running locally — see Section 9)
