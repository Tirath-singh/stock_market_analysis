
# src/predict.py

from pathlib import Path

import joblib
import pandas as pd


# 1. Set project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "etf_classification_model.joblib"
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "stock_market_clean.csv"


# 2. Load the trained model and dataset
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}\n"
        "Run the model-saving cell in 03_modeling.ipynb first."
    )

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

# These are the same features used during model training
feature_columns = list(model.feature_names_in_)

print("\n===== ETF CLASSIFICATION PREDICTION =====")
print("Enter the details of a security below.")
print("For categorical fields, press Enter to use the most common value.\n")


# 3. Collect input for each feature
record = {}

for column in feature_columns:

    print(f"\nFeature: {column}")

    # Numeric input
    if pd.api.types.is_numeric_dtype(df[column]):
        default_value = df[column].median()

        while True:
            user_value = input(
                f"Enter {column} (default {default_value}): "
            ).strip()

            if user_value == "":
                record[column] = default_value
                break

            try:
                record[column] = float(user_value)
                break
            except ValueError:
                print("Please enter a valid number.")

    # Categorical input
    else:
        valid_values = (
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        print("Available values:", ", ".join(valid_values))

        default_value = (
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
            .mode()
            .iloc[0]
        )

        user_value = input(
            f"Enter {column} (default {default_value}): "
        ).strip()

        if user_value == "":
            record[column] = default_value
        else:
            # Use the original category spelling from the dataset
            matched_value = next(
                (
                    value for value in valid_values
                    if value.casefold() == user_value.casefold()
                ),
                None
            )

            if matched_value is None:
                print(
                    f"Unknown value for {column}. "
                    f"Using default: {default_value}"
                )
                record[column] = default_value
            else:
                record[column] = matched_value


# 4. Arrange inputs in the training feature order
input_df = pd.DataFrame([record], columns=feature_columns)

print("\nInput record:")
print(input_df.to_string(index=False))


# 5. Predict ETF or Non-ETF
prediction = int(model.predict(input_df)[0])

label = "ETF" if prediction == 1 else "Non-ETF"

print("\n===== PREDICTION RESULT =====")
print(f"Predicted class: {label}")

# Show model probability, if supported
if hasattr(model, "predict_proba"):
    probabilities = model.predict_proba(input_df)[0]
    class_labels = list(model.named_steps["model"].classes_)

    probability_by_class = dict(zip(class_labels, probabilities))

    print(
        f"Probability of Non-ETF: "
        f"{probability_by_class.get(0, 0) * 100:.2f}%"
    )
    print(
        f"Probability of ETF: "
        f"{probability_by_class.get(1, 0) * 100:.2f}%"
    )

print("\nNote: These are model estimates, not guaranteed outcomes.")
