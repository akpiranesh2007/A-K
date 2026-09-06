import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Maintenance Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM THEME
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0F1020;
    color: #F5F5F7;
}

section[data-testid="stSidebar"] {
    background-color: #17182B;
    border-right: 1px solid #303252;
}

section[data-testid="stSidebar"] * {
    color: #F5F5F7;
}

h1 {
    color: #7C83FD !important;
    font-weight: 700 !important;
}

h2 {
    color: #67E8F9 !important;
}

h3 {
    color: #C4B5FD !important;
}

p, label {
    color: #E5E7EB !important;
}

div[data-testid="metric-container"] {
    background-color: #191B32;
    border: 1px solid #34365A;
    border-radius: 14px;
    padding: 15px;
}

div[data-testid="metric-container"] label {
    color: #A5B4FC !important;
}

div[data-testid="metric-container"] div {
    color: #67E8F9 !important;
}

.stButton > button {
    background-color: #6366F1;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #7C3AED;
    color: white;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #34365A;
    border-radius: 12px;
}

input, textarea {
    background-color: #191B32 !important;
    color: white !important;
    border: 1px solid #3B3D66 !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] > div {
    background-color: #191B32;
    border: 1px solid #3B3D66;
    border-radius: 8px;
}

code {
    color: #67E8F9 !important;
}

hr {
    border-color: #303252;
}

.project-banner {
    background: linear-gradient(
        135deg,
        #312E81,
        #4C1D95,
        #155E75
    );
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 25px;
    border: 1px solid #6366F1;
}

.project-banner h1 {
    color: white !important;
    margin-bottom: 5px;
}

.project-banner p {
    color: #CFFAFE !important;
    font-size: 17px;
}

.feature-card {
    background-color: #191B32;
    border: 1px solid #34365A;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    pull_requests = pd.read_csv(
        DATA_DIR / "pull_requests.csv"
    )

    incidents = pd.read_csv(
        DATA_DIR / "incidents.csv"
    )

    code_diffs = pd.read_csv(
        DATA_DIR / "code_diffs.csv"
    )

    reviews = pd.read_csv(
        DATA_DIR / "reviews.csv"
    )

    return (
        pull_requests,
        incidents,
        code_diffs,
        reviews
    )


try:

    (
        pull_requests,
        incidents,
        code_diffs,
        reviews
    ) = load_data()

except Exception as e:

    st.error("❌ Project data could not be loaded.")

    st.markdown("""
    ### Required folder structure

    ```
    maintenance-knowledge-assistant/
    │
    ├── app.py
    ├── README.md
    ├── requirements.txt
    │
    └── data/
        ├── pull_requests.csv
        ├── incidents.csv
        ├── code_diffs.csv
        └── reviews.csv
    ```
    """)

    st.error(f"Error: {e}")

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "runbooks" not in st.session_state:
    st.session_state.runbooks = []

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

if "api_records" not in st.session_state:
    st.session_state.api_records = []

if "rollback_log" not in st.session_state:
    st.session_state.rollback_log = []

if "experiment_results" not in st.session_state:
    st.session_state.experiment_results = []

if "approved_runbooks" not in st.session_state:
    st.session_state.approved_runbooks = []


# ============================================================
# AUDIT FUNCTION
# ============================================================

def add_audit(action, pr_id, details):

    st.session_state.audit_log.append({

        "Timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "Action":
            action,

        "PR_ID":
            pr_id,

        "Details":
            details
    })


# ============================================================
# RISK CHECKER
# ============================================================

def is_high_impact(text):

    keywords = [
        "authentication",
        "security",
        "password",
        "permission",
        "database",
        "payment",
        "delete",
        "production"
    ]

    text = str(text).lower()

    return any(
        keyword in text
        for keyword in keywords
    )


# ============================================================
# RUNBOOK GENERATOR
# ============================================================

def generate_runbook(pr_id):

    pr_rows = pull_requests[
        pull_requests["PR_ID"] == pr_id
    ]

    if len(pr_rows) == 0:

        return {
            "error": "Pull Request not found."
        }

    pr = pr_rows.iloc[0]


    incident_rows = incidents[
        incidents["PR_ID"] == pr_id
    ]


    diff_rows = code_diffs[
        code_diffs["PR_ID"] == pr_id
    ]


    review_rows = reviews[
        reviews["PR_ID"] == pr_id
    ]


    # --------------------------------------------------------
    # INCIDENT
    # --------------------------------------------------------

    if len(incident_rows) == 0:

        incident_problem = (
            "Incident information is missing."
        )

        incident_discussion = (
            "Root cause cannot be fully verified."
        )

        incident_available = False

    else:

        incident = incident_rows.iloc[0]

        incident_problem = incident["Problem"]

        incident_discussion = incident["Discussion"]

        incident_available = True


    # --------------------------------------------------------
    # CODE DIFF
    # --------------------------------------------------------

    if len(diff_rows) == 0:

        changed_file = "Code diff unavailable."

        old_code = "Not available."

        new_code = "Not available."

        diff_available = False

    else:

        diff = diff_rows.iloc[0]

        changed_file = diff["File"]

        old_code = diff["Old_Code"]

        new_code = diff["New_Code"]

        diff_available = True


    # --------------------------------------------------------
    # REVIEW
    # --------------------------------------------------------

    if len(review_rows) == 0:

        reviewer_status = "Unknown"

        verification = (
            "Reviewer information unavailab
