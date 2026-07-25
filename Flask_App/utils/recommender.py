# =====================================================
# MindSense AI Recommendation Engine
# =====================================================

def generate_recommendations(form_data, prediction):

    recommendations = []

    # =================================================
    # High Risk Recommendations
    # =================================================

    if prediction == "High Risk":

        recommendations.extend([

            "Consult a qualified mental health professional for a comprehensive assessment.",

            "Share your feelings with a trusted family member, friend, or mentor.",

            "Avoid dealing with emotional stress alone and seek support when needed."

        ])

    # =================================================
    # Sleep Duration
    # =================================================

    sleep = form_data.get("Sleep Duration", "")

    if sleep == "Less than 5 hours":

        recommendations.append(
            "Aim for at least 7–8 hours of quality sleep every night."
        )

    elif sleep == "5-6 hours":

        recommendations.append(
            "Try to increase your sleep duration to improve mental well-being."
        )

    # =================================================
    # Financial Stress
    # =================================================

    financial = float(form_data.get("Financial Stress", 0))

    if financial >= 4:

        recommendations.append(
            "Consider creating a financial plan or discussing concerns with a financial advisor."
        )

    elif financial >= 2:

        recommendations.append(
            "Monitor your financial stress and maintain a monthly budget."
        )

    # =================================================
    # Academic Pressure
    # =================================================

    academic = float(form_data.get("Academic Pressure", 0))

    if academic >= 4:

        recommendations.append(
            "Break study sessions into smaller goals and take regular breaks."
        )

    elif academic >= 2:

        recommendations.append(
            "Practice effective time management to reduce academic stress."
        )

    # =================================================
    # Work Pressure
    # =================================================

    work = float(form_data.get("Work Pressure", 0))

    if work >= 4:

        recommendations.append(
            "Discuss workload concerns with your manager or mentor if possible."
        )

    elif work >= 2:

        recommendations.append(
            "Take short breaks during work and maintain a healthy work-life balance."
        )

    # =================================================
    # Study Satisfaction
    # =================================================

    study = float(form_data.get("Study Satisfaction", 5))

    if study <= 2:

        recommendations.append(
            "Seek academic guidance or tutoring if you are struggling with your studies."
        )

    # =================================================
    # Job Satisfaction
    # =================================================

    job = float(form_data.get("Job Satisfaction", 5))

    if job <= 2:

        recommendations.append(
            "Reflect on workplace challenges and discuss career development opportunities."
        )

    # =================================================
    # Work / Study Hours
    # =================================================

    hours = float(form_data.get("Work/Study Hours", 0))

    if hours >= 10:

        recommendations.append(
            "Avoid excessive work or study hours and schedule regular breaks."
        )

    # =================================================
    # Dietary Habits
    # =================================================

    diet = form_data.get("Dietary Habits", "")

    if diet == "Unhealthy":

        recommendations.append(
            "Maintain a balanced diet, stay hydrated, and reduce processed food intake."
        )

    elif diet == "Moderate":

        recommendations.append(
            "Include more fruits, vegetables, and protein-rich foods in your meals."
        )

    # =================================================
    # Family History
    # =================================================

    if form_data.get("Family History of Mental Illness") == "Yes":

        recommendations.append(
            "Regular mental health check-ups may help with early identification of symptoms."
        )

    # =================================================
    # Suicidal Thoughts
    # =================================================

    if form_data.get("Have you ever had suicidal thoughts ?") == "Yes":

        recommendations.extend([

            "Please seek immediate support from a qualified mental health professional.",

            "Reach out to a trusted family member or friend today.",

            "If you feel you are in immediate danger, contact your local emergency services or crisis support line."

        ])

    # =================================================
    # Healthy Lifestyle Recommendation
    # =================================================

    recommendations.append(
        "Engage in at least 30 minutes of physical activity most days of the week."
    )

    recommendations.append(
        "Practice mindfulness, meditation, or deep breathing exercises regularly."
    )

    # =================================================
    # Remove Duplicate Recommendations
    # =================================================

    recommendations = list(dict.fromkeys(recommendations))

    # =================================================
    # Low Risk Default Recommendations
    # =================================================

    if prediction == "Low Risk" and len(recommendations) <= 2:

        recommendations.extend([

            "Maintain your healthy lifestyle and regular daily routine.",

            "Continue exercising regularly and eating a balanced diet.",

            "Stay socially connected with friends and family.",

            "Take regular breaks during work or study to avoid burnout."

        ])

    return recommendations