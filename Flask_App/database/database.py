import sqlite3
import os
from datetime import datetime

# =====================================================
# Database Configuration
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "database", "mindsense.db")


# =====================================================
# Database Connection
# =====================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================
# Create Table
# =====================================================

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            assessment_date TEXT,

            prediction TEXT,

            confidence REAL,

            low_probability REAL,

            high_probability REAL

        )
    """)

    conn.commit()
    conn.close()


# =====================================================
# Save Assessment
# =====================================================

def save_assessment(result):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO assessments(

            assessment_date,
            prediction,
            confidence,
            low_probability,
            high_probability

        )

        VALUES(?,?,?,?,?)

    """, (

        datetime.now().strftime("%d-%m-%Y %H:%M"),

        result["prediction"],

        result["confidence"],

        result["probability"][0],

        result["probability"][1]

    ))

    conn.commit()
    conn.close()


# =====================================================
# Dashboard Statistics
# =====================================================

def get_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # Total Assessments
    # -----------------------------

    cursor.execute("SELECT COUNT(*) FROM assessments")
    total = cursor.fetchone()[0]

    # -----------------------------
    # Low Risk
    # -----------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM assessments
        WHERE prediction='Low Risk'
    """)
    low = cursor.fetchone()[0]

    # -----------------------------
    # High Risk
    # -----------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM assessments
        WHERE prediction='High Risk'
    """)
    high = cursor.fetchone()[0]

    # -----------------------------
    # Average Confidence
    # -----------------------------

    cursor.execute("""
        SELECT AVG(confidence)
        FROM assessments
    """)

    avg = cursor.fetchone()[0]

    if avg is None:
        avg = 0

    conn.close()

    return {

        "total": total,

        "low": low,

        "high": high,

        "avg_confidence": round(avg, 2)

    }


# =====================================================
# Recent Assessments
# =====================================================

def get_recent_assessments(limit=5):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM assessments

        ORDER BY id DESC

        LIMIT ?

    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows