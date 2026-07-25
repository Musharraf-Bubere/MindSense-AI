from flask import Flask, render_template, request, send_from_directory

from utils.predictor import predict_risk
from utils.pdf_generator import generate_pdf

from database.database import (
    create_table,
    save_assessment,
    get_dashboard_stats,
    get_recent_assessments
)

# =====================================================
# App Configuration
# =====================================================

app = Flask(__name__)

latest_result = None

create_table()


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():
    return render_template("home.html")


# =====================================================
# ASSESSMENT
# =====================================================

@app.route("/assessment")
def assessment():
    return render_template("assessment.html")


# =====================================================
# PREDICT
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():

    global latest_result

    try:

        form_data = request.form.to_dict()

        result = predict_risk(form_data)

        # Save into database
        save_assessment(result)

        # Store latest result for PDF download
        latest_result = result

        return render_template(

            "result.html",

            prediction=result["prediction"],

            prediction_class=result["prediction_class"],

            confidence=result["confidence"],

            probability=result["probability"],

            recommendations=result["recommendations"],

            top_features=result["top_features"],

            chart=result["chart"]

        )

    except Exception as e:

        return f"""
        <h2>Prediction Error</h2>
        <p>{e}</p>
        <a href='/assessment'>Go Back</a>
        """


# =====================================================
# DOWNLOAD PDF
# =====================================================

@app.route("/download-report")
def download_report():

    global latest_result

    if latest_result is None:
        return "No assessment available."

    filename = generate_pdf(latest_result)

    return send_from_directory(

        "static/reports",

        filename,

        as_attachment=True

    )


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
def dashboard():

    stats = get_dashboard_stats()

    recent = get_recent_assessments()

    return render_template(

        "dashboard.html",

        total=stats["total"],

        low=stats["low"],

        high=stats["high"],

        avg_confidence=stats["avg_confidence"],

        recent=recent

    )


# =====================================================
# ABOUT
# =====================================================

@app.route("/about")
def about():
    return render_template("about.html")


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    app.run(debug=True)