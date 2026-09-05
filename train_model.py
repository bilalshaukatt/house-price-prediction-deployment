import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report

# "None" is a real category here (no alley, no pool, etc.), not missing data
df = pd.read_csv('/mnt/user-data/uploads/Week_3_FINAL_CLEANED.csv', keep_default_na=False, na_values=[''])

# Binary target: is this house priced above the median? (Expensive vs Affordable)
median_price = df['SalePrice'].median()
df['PriceCategory'] = (df['SalePrice'] > median_price).astype(int)

# Compact, intuitive feature set for a usable web form
numeric_features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF',
                     'FullBath', 'YearBuilt', 'YearRemodAdd', 'LotArea', 'Fireplaces']
categorical_features = ['Neighborhood', 'HouseStyle', 'ExterQual', 'KitchenQual']

features = numeric_features + categorical_features
X = df[features].copy()
y = df['PriceCategory']

for c in numeric_features:
    X[c] = pd.to_numeric(X[c], errors='coerce')

preprocessor = ColumnTransformer(transformers=[
    ('num', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]), numeric_features),
    ('cat', Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ]), categorical_features)
])

model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_split=5, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Test accuracy: {acc:.4f}")
print(classification_report(y_test, y_pred, target_names=['Affordable', 'Expensive']))

joblib.dump(model, '/home/claude/ml_task/house_price_model.pkl')
joblib.dump({
    'numeric_features': numeric_features,
    'categorical_features': categorical_features,
    'median_price': float(median_price),
    'categorical_options': {c: sorted(df[c].fillna('Unknown').unique().tolist()) for c in categorical_features},
    'numeric_ranges': {c: (float(X[c].min()), float(X[c].max()), float(X[c].median())) for c in numeric_features},
    'test_accuracy': float(acc)
}, '/home/claude/ml_task/model_metadata.pkl')

print("Saved model and metadata.")
