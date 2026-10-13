
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# -----------------------------------------
# 1. Project paths - according to your structure
# -----------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent

DATA_PATH = PROJECT_ROOT / "Data" / "stock_market.csv.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "etf_classification_model.joblib"


# -----------------------------------------
# 2. Page setup
# -----------------------------------------
st.set_page_config(
    page_title="Stock Market ETF Classification",
    page_icon="📈",
    layout="centered"
)

st.title(" Stock Market ETF Classification")

st.write(
    "Enter security listing details to predict "
    "whether a security is an ETF or a Non-ETF."
)

st.info(
    "This model classifies ETF status. "
    "It does not predict future stock prices."
)


# -----------------------------------------
# 3. Check files
# -----------------------------------------
if not DATA_PATH.exists():
    st.error(f"Dataset file not found: {DATA_PATH}")
    st.stop()

if not MODEL_PATH.exists():
    st.error(f"Trained model not found: {MODEL_PATH}")
    st.stop()


# -----------------------------------------
# 4. Load dataset and trained model
# -----------------------------------------
@st.cache_data
def load_data(path):
    return pd.read_csv(path)


@st.cache_resource
def load_model(path):
    return joblib.load(path)


df = load_data(str(DATA_PATH))
model = load_model(str(MODEL_PATH))

# Get the exact feature order used during training
feature_columns = list(model.feature_names_in_)


# -----------------------------------------
# 5. Prediction form
# -----------------------------------------
st.subheader("Enter Security Details")

record = {}

with st.form("etf_prediction_form"):

    for column in feature_columns:

        if column not in df.columns:
            st.error(
                f"Column '{column}' is missing from the CSV file. "
                "The dataset must contain the model's training features."
            )
            st.stop()

        if pd.api.types.is_numeric_dtype(df[column]):

            median_value = df[column].median()

            if pd.isna(median_value):
                median_value = 0.0

            record[column] = st.number_input(
                column,
                value=float(median_value)
            )

        else:
            values = (
                df[column]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                .tolist()
            )

            values = sorted(values)

            if not values:
                values = ["Unknown"]

            modes = (
                df[column]
                .dropna()
                .astype(str)
                .str.strip()
                .mode()
            )

            default_value = (
                modes.iloc[0] if not modes.empty else values[0]
            )

            default_index = (
                values.index(default_value)
                if default_value in values
                else 0
            )

            record[column] = st.selectbox(
                column,
                options=values,
                index=default_index
            )

    submitted = st.form_submit_button(
        "Predict ETF Status",
        use_container_width=True
    )


# -----------------------------------------
# 6. Make prediction
# -----------------------------------------
if submitted:

    input_df = pd.DataFrame(
        [record],
        columns=feature_columns
    )

    prediction = int(model.predict(input_df)[0])

    st.divider()
    st.subheader("Prediction Result")

    if prediction == 1:
        st.success("Predicted Class: ETF")
    else:
        st.success("Predicted Class: Non-ETF")

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_df)[0]
        classes = list(model.named_steps["model"].classes_)

        probability_map = dict(zip(classes, probabilities))

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "ETF Model Probability",
                f"{probability_map.get(1, 0) * 100:.2f}%"
            )

        with col2:
            st.metric(
                "Non-ETF Model Probability",
                f"{probability_map.get(0, 0) * 100:.2f}%"
            )

        st.caption(
            "Probabilities are model estimates, not guarantees."
        )

    with st.expander("View Input Details"):
        st.dataframe(input_df, use_container_width=True)