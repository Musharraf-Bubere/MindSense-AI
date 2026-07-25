import os
import uuid
import joblib
import shap
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ======================================================
# Load Model
# ======================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "Models", "logistic_regression.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "Models", "feature_columns.pkl")
BACKGROUND_PATH = os.path.join(BASE_DIR, "Models", "X_train_background.pkl")

model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURE_PATH)
background = joblib.load(BACKGROUND_PATH)

explainer = shap.Explainer(model, background)


# ======================================================
# SHAP Table
# ======================================================

def get_shap_explanation(input_data, top_n=5):

    shap_values = explainer(input_data)

    values = shap_values.values[0]

    df = pd.DataFrame({

        "Feature": input_data.columns,

        "SHAP Value": values

    })

    df["Absolute"] = df["SHAP Value"].abs()

    df = df.sort_values(

        by="Absolute",

        ascending=False

    )

    return df.head(top_n)


# ======================================================
# SHAP Chart
# ======================================================

def create_shap_chart(input_data):

    shap_df = get_shap_explanation(input_data)

    plt.figure(figsize=(8,4))

    colors = [

        "#EF4444" if x > 0 else "#22C55E"

        for x in shap_df["SHAP Value"]

    ]

    plt.barh(

        shap_df["Feature"],

        shap_df["SHAP Value"],

        color=colors

    )

    plt.xlabel("SHAP Value")

    plt.title("Top Factors Influencing Prediction")

    plt.gca().invert_yaxis()

    filename = f"{uuid.uuid4().hex}.png"

    save_path = os.path.join(

        BASE_DIR,

        "static",

        "charts",

        filename

    )

    os.makedirs(

        os.path.dirname(save_path),

        exist_ok=True

    )

    plt.tight_layout()

    plt.savefig(save_path)

    plt.close()

    return f"charts/{filename}"