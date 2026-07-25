import os
import joblib
import pandas as pd

from utils.recommender import generate_recommendations
from utils.shap_helper import get_shap_explanation, create_shap_chart


# =====================================================
# Load Model & Feature Columns
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "Models", "logistic_regression.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "Models", "feature_columns.pkl")

model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURE_PATH)


# =====================================================
# Prepare Input
# =====================================================

def prepare_input(form_data):

    # Create dataframe with all features initialized to 0.0
    input_data = pd.DataFrame(
        0.0,
        index=[0],
        columns=feature_columns
    )

    # =================================================
    # Numeric Features
    # =================================================

    numeric_features = [
        "Age",
        "Academic Pressure",
        "Work Pressure",
        "CGPA",
        "Study Satisfaction",
        "Job Satisfaction",
        "Work/Study Hours",
        "Financial Stress"
    ]

    for feature in numeric_features:

        value = form_data.get(feature)

        if value not in [None, ""]:

            input_data.at[0, feature] = float(value)

    # =================================================
    # Binary Features
    # =================================================

    input_data.at[0, "Gender"] = (
        1 if form_data.get("Gender") == "Male" else 0
    )

    input_data.at[0, "Working Professional or Student"] = (
        1 if form_data.get("Working Professional or Student")
        == "Working Professional"
        else 0
    )

    input_data.at[0, "Family History of Mental Illness"] = (
        1 if form_data.get("Family History of Mental Illness") == "Yes"
        else 0
    )

    input_data.at[0, "Have you ever had suicidal thoughts ?"] = (
        1 if form_data.get("Have you ever had suicidal thoughts ?") == "Yes"
        else 0
    )

    # =================================================
    # Sleep Duration
    # =================================================

    sleep_mapping = {
        "Less than 5 hours": 0,
        "5-6 hours": 1,
        "7-8 hours": 2,
        "More than 8 hours": 3
    }

    input_data.at[0, "Sleep Duration"] = sleep_mapping.get(
        form_data.get("Sleep Duration"),
        0
    )

    # =================================================
    # Dietary Habits
    # =================================================

    diet_mapping = {
        "Unhealthy": 0,
        "Moderate": 1,
        "Healthy": 2
    }

    input_data.at[0, "Dietary Habits"] = diet_mapping.get(
        form_data.get("Dietary Habits"),
        0
    )

    # =================================================
    # One-Hot Encoding
    # =================================================

    city = form_data.get("City")
    profession = form_data.get("Profession")
    degree = form_data.get("Degree")

    city_column = f"City_{city}"
    profession_column = f"Profession_{profession}"
    degree_column = f"Degree_{degree}"

    if city_column in input_data.columns:
        input_data.at[0, city_column] = 1

    if profession_column in input_data.columns:
        input_data.at[0, profession_column] = 1

    if degree_column in input_data.columns:
        input_data.at[0, degree_column] = 1

    return input_data


# =====================================================
# Prediction
# =====================================================

def predict_risk(form_data):

    # Prepare model input
    input_data = prepare_input(form_data)

    # Model prediction
    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0]

    confidence = round(max(probability) * 100, 2)

    # Risk label
    risk = "High Risk" if prediction == 1 else "Low Risk"

    # SHAP Explanation
    top_features = get_shap_explanation(input_data)

    # SHAP Chart
    chart = create_shap_chart(input_data)

    # Personalized Recommendations
    recommendations = generate_recommendations(
        form_data,
        risk
    )

    return {

        "prediction": risk,

        "prediction_class": int(prediction),

        "confidence": confidence,

        "probability": probability.tolist(),

        "recommendations": recommendations,

        "top_features": top_features.to_dict(
            orient="records"
        ),

        "chart": chart

    }