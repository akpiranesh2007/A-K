import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Maintenance Knowledge Assistant",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL APPLICATION
       ====================================================== */

    .stApp {
        background-color: #0b1020 !important;
    }

    .main {
        background-color: #0b1020 !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ======================================================
       MAIN TEXT
       ====================================================== */

    .stApp p {
        color: #d1d5db !important;
    }

    .stApp li {
        color: #d1d5db !important;
    }

    .stApp label {
        color: #dbeafe !important;
    }


    /* ======================================================
       HEADINGS
       ====================================================== */

    .stApp h1 {
        color: #67e8f9 !important;
        font-weight: 700 !important;
    }

    .stApp h2 {
        color: #7dd3fc !important;
        font-weight: 650 !important;
    }

    .stApp h3 {
        color: #a5f3fc !important;
        font-weight: 600 !important;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #334155 !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #111827 !important;
    }

    section[data-testid="stSidebar"] h1 {
        color: #67e8f9 !important;
    }

    section[data-testid="stSidebar"] h2 {
        color: #7dd3fc !important;
    }

    section[data-testid="stSidebar"] h3 {
        color: #a5f3fc !important;
    }

    section[data-testid="stSidebar"] p {
        color: #94a3b8 !important;
    }

    section[data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] span {
        color: #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        color: #e2e8f0 !important;
    }


    /* ======================================================
       TITLE CARD
       ====================================================== */

    .title-box {
        padding: 30px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #171554,
            #1e1b4b
        );
        border: 1px solid #4f46e5;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.30);
    }

    .title-box h1 {
        color: #67e8f9 !important;
        margin-bottom: 10px;
    }

    .title-box p {
        color: #cbd5e1 !important;
        font-size: 16px;
    }


    /* ======================================================
       INFORMATION CARD
       ====================================================== */

    .info-box {
        padding: 20px;
        border-radius: 14px;
        background-color: #172554;
        border: 1px solid #2563eb;
        margin-bottom: 18px;
    }

    .info-box b {
        color: #67e8f9 !important;
    }

    .info-box p {
        color: #dbeafe !important;
    }


    /* ======================================================
       METRIC CARDS
       ====================================================== */

    [data-testid="stMetric"] {
        background-color: #111827 !important;
        border: 1px solid #334155 !important;
        padding: 18px !important;
        border-radius: 14px !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #67e8f9 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #cbd5e1 !important;
    }


    /* ======================================================
       TEXT INPUT
       ====================================================== */

    .stTextInput input {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }

    .stTextInput input:focus {
        border-color: #67e8f9 !important;
        box-shadow: 0 0 0 1px #67e8f9 !important;
    }


    /* ======================================================
       TEXT AREA
       ====================================================== */

    .stTextArea textarea {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }

    .stTextArea textarea:focus {
        border-color: #67e8f9 !important;
        box-shadow: 0 0 0 1px #67e8f9 !important;
    }


    /* ======================================================
       NUMBER INPUT
       ====================================================== */

    .stNumberInput input {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }


    /* ======================================================
       SELECT BOX
       ====================================================== */

    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border-color: #475569 !important;
    }

    div[data-baseweb="select"] span {
        color: #f8fafc !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton button {
        background-color: #4f46e5 !important;
        color: #ffffff !important;
        border: 1px solid #6366f1 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .stButton button:hover {
        background-color: #6366f1 !important;
        color: #ffffff !important;
        border-color: #818cf8 !important;
    }


    /* ======================================================
       CHECKBOX
       ====================================================== */

    .stCheckbox label {
        color: #e2e8f0 !important;
    }


    /* ======================================================
       RADIO
       ====================================================== */

    .stRadio label {
        color: #e2e8f0 !important;
    }


    /* ======================================================
       DATAFRAME
       ====================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }


    /* ======================================================
       CODE BLOCK
       ====================================================== */

    [data-testid="stCodeBlock"] {
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }


    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {
        border-color: #334155 !important;
    }


    /* ======================================================
       ALERTS
       ====================================================== */

    [data-testid="stAlert"] {
        border-radius: 10px !important;
    }


    /* ======================================================
       SCROLLBAR
       ====================================================== */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #0b1020;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# ============================================================
# PERSISTENT SQLITE STORAGE
# ============================================================

# The database is created automatically when the app starts.
# It is stored inside the existing data folder so the original
# CSV files are preserved.
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "maintenance_assistant.db"


def get_db_connection():
    return sqlite3.connect(DB_PATH)


def init_database():
    """Create/migrate SQLite tables without relying on a UNIQUE constraint.

    Older versions of the prototype created different runbook schemas.
    The migration below adds every field the current app needs and does not
    require the old pr_id column to have a UNIQUE constraint.
    """

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS runbooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pr_id TEXT,
            title TEXT,
            problem TEXT,
            root_cause TEXT,
            solution TEXT,
            incident_resolution TEXT,
            changed_file TEXT,
            old_code TEXT,
            new_code TEXT,
            reviewer TEXT,
            reviewer_status TEXT,
            verification TEXT,
            verification_status TEXT,
            confidence REAL,
            high_impact INTEGER,
            trust_status TEXT DEFAULT 'PENDING HUMAN APPROVAL',
            created_at TEXT,
            data TEXT
        )
    """)

    # Migrate ANY older runbook schema in place. We never delete the user's
    # existing runbook rows and we do not depend on pr_id being UNIQUE.
    existing_columns = {
        row[1] for row in cur.execute("PRAGMA table_info(runbooks)").fetchall()
    }

    migration_columns = {
        "pr_id": "TEXT",
        "title": "TEXT",
        "problem": "TEXT",
        "root_cause": "TEXT",
        "solution": "TEXT",
        "incident_resolution": "TEXT",
        "changed_file": "TEXT",
        "old_code": "TEXT",
        "new_code": "TEXT",
        "reviewer": "TEXT",
        "reviewer_status": "TEXT",
        "verification": "TEXT",
        "verification_status": "TEXT",
        "confidence": "REAL",
        "high_impact": "INTEGER",
        "trust_status": "TEXT",
        "created_at": "TEXT",
        "data": "TEXT",
    }

    for column, column_type in migration_columns.items():
        if column not in existing_columns:
            cur.execute(
                f"ALTER TABLE runbooks ADD COLUMN {column} {column_type}"
            )

    cur.execute("""
        CREATE TABLE IF NOT EXISTS validation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_case TEXT,
            tester_id TEXT,
            baseline_minutes REAL,
            assistant_minutes REAL,
            time_saved REAL,
            reduction_percent REAL,
            result TEXT,
            correctness TEXT,
            observation TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rollback_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pr_id TEXT,
            reason TEXT,
            timestamp TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def db_add_audit(action, details):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO audit_log (timestamp, action, details) VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), action, details)
    )
    conn.commit()
    conn.close()


def db_save_runbook(runbook):
    """Save a complete runbook safely across old and new SQLite schemas.

    IMPORTANT: Do NOT use `ON CONFLICT(pr_id)` here. Older databases may not
    have a UNIQUE constraint on pr_id, and SQLite then raises:
    "ON CONFLICT clause does not match any PRIMARY KEY or UNIQUE constraint".
    We instead find the existing row by pr_id and update it, or insert it.
    """

    import json

    conn = get_db_connection()

    try:
        pr_id = str(runbook.get("PR_ID", ""))
        created_at = runbook.get(
            "Created At",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        payload = json.dumps(runbook, ensure_ascii=False)

        values = (
            pr_id,
            runbook.get("Title", ""),
            runbook.get("Problem", ""),
            runbook.get("Root Cause", ""),
            runbook.get("Solution", ""),
            runbook.get("Incident Resolution", ""),
            runbook.get("Changed File", ""),
            runbook.get("Old Code", ""),
            runbook.get("New Code", ""),
            runbook.get("Reviewer", ""),
            runbook.get("Reviewer Status", ""),
            runbook.get("Verification", ""),
            runbook.get("Verification Status", ""),
            float(runbook.get("Confidence", 0) or 0),
            int(bool(runbook.get("High Impact", False))),
            runbook.get("Trust Status", "PENDING HUMAN APPROVAL"),
            created_at,
            payload,
        )

        existing = conn.execute(
            "SELECT id FROM runbooks WHERE pr_id = ? ORDER BY id LIMIT 1",
            (pr_id,)
        ).fetchone()

        if existing is not None:
            conn.execute(
                """
                UPDATE runbooks
                SET pr_id = ?, title = ?, problem = ?, root_cause = ?,
                    solution = ?, incident_resolution = ?, changed_file = ?,
                    old_code = ?, new_code = ?, reviewer = ?,
                    reviewer_status = ?, verification = ?,
                    verification_status = ?, confidence = ?, high_impact = ?,
                    trust_status = ?, created_at = ?, data = ?
                WHERE id = ?
                """,
                values + (existing[0],)
            )
        else:
            conn.execute(
                """
                INSERT INTO runbooks (
                    pr_id, title, problem, root_cause, solution,
                    incident_resolution, changed_file, old_code, new_code,
                    reviewer, reviewer_status, verification,
                    verification_status, confidence, high_impact,
                    trust_status, created_at, data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                values
            )

        conn.commit()

    finally:
        conn.close()


def db_save_validation(experiment):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO validation_results (
            test_case, tester_id, baseline_minutes, assistant_minutes,
            time_saved, reduction_percent, result, correctness, observation, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        experiment.get("Test Case", ""),
        experiment.get("Tester ID", ""),
        experiment.get("Baseline Minutes", 0),
        experiment.get("Assistant Minutes", 0),
        experiment.get("Time Saved", 0),
        experiment.get("Reduction %", 0),
        experiment.get("Result", ""),
        experiment.get("Recommendation Correctness", ""),
        experiment.get("Observation", ""),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()


def db_delete_validation(validation_id):
    conn = get_db_connection()
    try:
        conn.execute(
            "DELETE FROM validation_results WHERE id = ?",
            (int(validation_id),)
        )
        conn.commit()
    finally:
        conn.close()


def db_save_rollback(record):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO rollback_log (pr_id, reason, timestamp, status) VALUES (?, ?, ?, ?)",
        (record.get("PR_ID", ""), record.get("Reason", ""), record.get("Timestamp", ""), record.get("Status", ""))
    )
    conn.commit()
    conn.close()


def load_persistent_state():
    conn = get_db_connection()
    audit = pd.read_sql_query(
        "SELECT timestamp AS Timestamp, action AS Action, details AS Details FROM audit_log ORDER BY id", conn
    ).to_dict("records")
    rollbacks = pd.read_sql_query(
        "SELECT pr_id AS PR_ID, reason AS Reason, timestamp AS Timestamp, status AS Status FROM rollback_log ORDER BY id", conn
    ).to_dict("records")
    validations = pd.read_sql_query(
        "SELECT id AS 'Validation ID', test_case AS 'Test Case', tester_id AS 'Tester ID', baseline_minutes AS 'Baseline Minutes', assistant_minutes AS 'Assistant Minutes', time_saved AS 'Time Saved', reduction_percent AS 'Reduction %', result AS Result, correctness AS 'Recommendation Correctness', observation AS Observation, created_at AS 'Created At' FROM validation_results ORDER BY id", conn
    ).to_dict("records")
    runbook_rows = pd.read_sql_query(
        "SELECT * FROM runbooks ORDER BY id", conn
    ).to_dict("records")
    conn.close()
    return audit, rollbacks, validations, runbook_rows


# Create the database immediately at application startup.
init_database()


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

    st.error("Unable to load the project data.")

    st.code(str(e))

    st.info(
        """
        Make sure your GitHub repository has this structure:

        data/
        ├── pull_requests.csv
        ├── incidents.csv
        ├── code_diffs.csv
        └── reviews.csv
        """
    )

    st.stop()


# ============================================================
# RESTORE COMPLETE RUNBOOKS FROM SQLITE + SOURCE CSV EVIDENCE
# ============================================================

def restore_runbook_from_saved_row(saved):

    pr_id = str(saved.get("pr_id", ""))

    pr_match = pull_requests[pull_requests["PR_ID"] == pr_id]
    incident_match = incidents[incidents["PR_ID"] == pr_id]
    diff_match = code_diffs[code_diffs["PR_ID"] == pr_id]
    review_match = reviews[reviews["PR_ID"] == pr_id]

    pr = pr_match.iloc[0] if not pr_match.empty else None
    incident = incident_match.iloc[0] if not incident_match.empty else None
    diff = diff_match.iloc[0] if not diff_match.empty else None
    review = review_match.iloc[0] if not review_match.empty else None

    # Values persisted in SQLite take priority; missing fields are
    # reconstructed from the original synthetic evidence CSVs.
    title = saved.get("title") or (str(pr["Title"]) if pr is not None else "")
    problem = saved.get("problem") or (
        str(incident["Problem"]) if incident is not None
        else (str(pr["Description"]) if pr is not None else "")
    )
    root_cause = saved.get("root_cause") or (
        str(incident["Discussion"]) if incident is not None else "Incident information unavailable."
    )
    solution = saved.get("solution") or (str(pr["Resolution"]) if pr is not None else "")
    incident_resolution = saved.get("incident_resolution") or (
        str(incident["Final_Resolution"]) if incident is not None else "Not available."
    )

    changed_file = saved.get("changed_file") or (
        str(diff["File"]) if diff is not None else "Code diff unavailable."
    )
    old_code = saved.get("old_code") or (
        str(diff["Old_Code"]) if diff is not None else "Not available."
    )
    new_code = saved.get("new_code") or (
        str(diff["New_Code"]) if diff is not None else "Not available."
    )

    reviewer = saved.get("reviewer") or (
        str(review["Reviewer"]) if review is not None else "Unavailable"
    )
    reviewer_status = saved.get("reviewer_status") or (
        str(review["Decision"]) if review is not None else "Unknown"
    )
    verification = saved.get("verification") or (
        str(review["Comment"]) if review is not None else "Reviewer information unavailable."
    )

    verification_status = saved.get("verification_status") or "Incomplete"
    confidence = saved.get("confidence", 0)
    high_impact = bool(saved.get("high_impact", 0))

    return {
        "PR_ID": pr_id,
        "Title": title,
        "Problem": problem,
        "Root Cause": root_cause,
        "Solution": solution,
        "Incident Resolution": incident_resolution,
        "Changed File": changed_file,
        "Old Code": old_code,
        "New Code": new_code,
        "Reviewer": reviewer,
        "Reviewer Status": reviewer_status,
        "Verification": verification,
        "Verification Status": verification_status,
        "Confidence": float(confidence or 0),
        "High Impact": high_impact,
        "Trust Status": saved.get("trust_status") or "PENDING HUMAN APPROVAL",
        "Created At": saved.get("created_at") or "",
    }


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

# Load persistent records once per Streamlit session.
if "persistent_state_loaded" not in st.session_state:
    (
        saved_audit,
        saved_rollbacks,
        saved_validations,
        saved_runbooks
    ) = load_persistent_state()

    st.session_state.audit_log = saved_audit
    st.session_state.rollback_log = saved_rollbacks
    st.session_state.experiment_results = saved_validations

    # Restore the complete runbook. Older SQLite rows may contain only
    # summary fields, so missing evidence is reconstructed from the
    # original synthetic CSV records.
    for saved in saved_runbooks:
        restored = restore_runbook_from_saved_row(saved)
        existing = [
            r for r in st.session_state.runbooks
            if r.get("PR_ID") == restored.get("PR_ID")
        ]
        if not existing:
            st.session_state.runbooks.append(restored)

    st.session_state.persistent_state_loaded = True


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def add_audit(action, details):

    event = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Action": action,
        "Details": details
    }

    st.session_state.audit_log.append(event)
    db_add_audit(action, details)


def is_high_impact(text):

    if text is None:
        return False

    text = str(text).lower()

    keywords = [
        "authentication",
        "security",
        "password",
        "permission",
        "database",
        "payment",
        "delete",
        "production",
        "credential",
        "access"
    ]

    return any(
        keyword in text
        for keyword in keywords
    )


def get_pr(pr_id):

    result = pull_requests[
        pull_requests["PR_ID"] == pr_id
    ]

    if result.empty:
        return None

    return result.iloc[0]


def get_incident(pr_id):

    result = incidents[
        incidents["PR_ID"] == pr_id
    ]

    if result.empty:
        return None

    return result.iloc[0]


def get_diff(pr_id):

    result = code_diffs[
        code_diffs["PR_ID"] == pr_id
    ]

    if result.empty:
        return None

    return result.iloc[0]


def get_review(pr_id):

    result = reviews[
        reviews["PR_ID"] == pr_id
    ]

    if result.empty:
        return None

    return result.iloc[0]


# ============================================================
# RUNBOOK GENERATOR
# ============================================================

def generate_runbook(pr_id):

    pr = get_pr(pr_id)
    incident = get_incident(pr_id)
    diff = get_diff(pr_id)
    review = get_review(pr_id)

    if pr is None:
        return None

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    confidence = 40

    if incident is not None:
        confidence += 15

    if diff is not None:
        confidence += 15

    if review is not None:

        if str(
            review["Decision"]
        ).lower() == "approved":

            confidence += 30

    confidence = min(
        confidence,
        100
    )

    # --------------------------------------------------------
    # Reviewer information
    # --------------------------------------------------------

    if review is None:

        reviewer_status = "Unknown"

        verification = (
            "Reviewer information unavailable."
        )

        reviewer_name = "Unavailable"

    else:

        reviewer_status = (
            str(review["Decision"])
        )

        verification = (
            str(review["Comment"])
        )

        reviewer_name = (
            str(review["Reviewer"])
        )

    # --------------------------------------------------------
    # Incident information
    # --------------------------------------------------------

    if incident is None:

        problem = str(
            pr["Description"]
        )

        root_cause = (
            "Incident information unavailable."
        )

        incident_resolution = (
            "Not available."
        )

    else:

        problem = str(
            incident["Problem"]
        )

        root_cause = str(
            incident["Discussion"]
        )

        incident_resolution = str(
            incident["Final_Resolution"]
        )

    # --------------------------------------------------------
    # Code diff
    # --------------------------------------------------------

    if diff is None:

        changed_file = (
            "Code diff unavailable."
        )

        old_code = "Not available."

        new_code = "Not available."

    else:

        changed_file = str(
            diff["File"]
        )

        old_code = str(
            diff["Old_Code"]
        )

        new_code = str(
            diff["New_Code"]
        )

    # --------------------------------------------------------
    # Verification
    # --------------------------------------------------------

    if incident is None or diff is None:

        verification_status = "Incomplete"

    elif review is None:

        verification_status = "Pending Review"

    elif str(
        review["Decision"]
    ).lower() != "approved":

        verification_status = "Pending Review"

    else:

        verification_status = "Verified"

    # --------------------------------------------------------
    # Risk
    # --------------------------------------------------------

    combined_text = (
        str(pr["Title"])
        + " "
        + str(pr["Description"])
        + " "
        + str(pr["Resolution"])
    )

    high_impact = is_high_impact(
        combined_text
    )

    # --------------------------------------------------------
    # Final Runbook
    # --------------------------------------------------------

    runbook = {

        "PR_ID":
            pr_id,

        "Title":
            str(pr["Title"]),

        "Problem":
            problem,

        "Root Cause":
            root_cause,

        "Solution":
            str(pr["Resolution"]),

        "Incident Resolution":
            incident_resolution,

        "Changed File":
            changed_file,

        "Old Code":
            old_code,

        "New Code":
            new_code,

        "Reviewer":
            reviewer_name,

        "Reviewer Status":
            reviewer_status,

        "Verification":
            verification,

        "Verification Status":
            verification_status,

        "Confidence":
            confidence,

        "High Impact":
            high_impact,

        "Trust Status":
            "PENDING HUMAN APPROVAL",

        "Created At":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }

    return runbook


# ============================================================
# MOCK API
# ============================================================

def mock_api_send(pr_id):

    pr = get_pr(pr_id)

    incident = get_incident(pr_id)

    diff = get_diff(pr_id)

    review = get_review(pr_id)

    payload = {

        "source":
            "Mock Engineering API",

        "timestamp":
            datetime.now().isoformat(),

        "pull_request":
            (
                pr.to_dict()
                if pr is not None
                else {}
            ),

        "incident":
            (
                incident.to_dict()
                if incident is not None
                else {}
            ),

        "code_diff":
            (
                diff.to_dict()
                if diff is not None
                else {}
            ),

        "review":
            (
                review.to_dict()
                if review is not None
                else {}
            )
    }

    st.session_state.api_records.append(
        payload
    )

    add_audit(
        "API Data Received",
        f"Mock engineering data received for {pr_id}"
    )

    return payload


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🛠️ Maintenance Assistant"
)

st.sidebar.caption(
    "Knowledge capture and verified runbook prototype"
)

st.sidebar.divider()

page = st.sidebar.radio(

    "Navigation",

    [
        "🏠 Dashboard",
        "📋 Pull Requests",
        "🚨 Incidents",
        "📘 Generate Runbook",
        "✅ Review Runbooks",
        "🔌 API Integration",
        "🔄 Rollback Manager",
        "⚠️ Risk Checker",
        "🧪 Edge Cases",
        "📝 Audit Trail",
        "📊 Validation Dashboard"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Prototype • Synthetic Data • Human-in-the-loop"
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="title-box">

        <h1>🛠️ Maintenance Knowledge Assistant</h1>

        <p>
        Convert completed engineering fixes into verified,
        reusable maintenance runbooks.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Pull Requests",
            len(pull_requests)
        )

    with col2:

        st.metric(
            "Incidents",
            len(incidents)
        )

    with col3:

        st.metric(
            "Code Diffs",
            len(code_diffs)
        )

    with col4:

        st.metric(
            "Reviews",
            len(reviews)
        )

    st.subheader(
        "🎯 Project Objective"
    )

    st.write(
        """
        When an engineer fixes a problem, the solution is often
        stored only inside a pull request, incident discussion,
        or code change.

        This assistant collects that evidence and converts it into
        a structured runbook that another engineer can reuse later.
        """
    )

    st.subheader(
        "🔄 System Workflow"
    )

    st.code(
        """
Engineering Data
       ↓
Mock API
       ↓
Evidence Extraction
       ↓
Runbook Generator
       ↓
Risk Checker
       ↓
Human Review
       ↓
Verified Runbook
       ↓
Audit Trail
       ↓
Validation
        """
    )

    st.markdown(
        """
        <div class="info-box">

        <b>Main Success Metric</b>

        <p>
        Reduce the time required for a new engineer
        to repeat a previously solved maintenance fix.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PULL REQUESTS
# ============================================================

elif page == "📋 Pull Requests":

    st.title(
        "📋 Pull Requests"
    )

    st.dataframe(
        pull_requests,
        use_container_width=True
    )

    st.subheader(
        "Pull Request Details"
    )

    pr_id = st.selectbox(
        "Select Pull Request",
        pull_requests["PR_ID"].tolist()
    )

    pr = get_pr(pr_id)

    if pr is not None:

        st.write(
            "### Title"
        )

        st.write(
            pr["Title"]
        )

        st.write(
            "### Description"
        )

        st.write(
            pr["Description"]
        )

        st.write(
            "### Resolution"
        )

        st.success(
            pr["Resolution"]
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                "Reviewer"
            )

            st.write(
                pr["Reviewer"]
            )

        with col2:

            st.write(
                "Status"
            )

            st.write(
                pr["Status"]
            )

        with col3:

            combined_text = (
                str(pr["Title"])
                + " "
                + str(pr["Description"])
                + " "
                + str(pr["Resolution"])
            )

            if is_high_impact(
                combined_text
            ):

                st.warning(
                    "⚠️ High Impact"
                )

            else:

                st.success(
                    "Normal Impact"
                )


# ============================================================
# INCIDENTS
# ============================================================

elif page == "🚨 Incidents":

    st.title(
        "🚨 Incident Discussions"
    )

    st.dataframe(
        incidents,
        use_container_width=True
    )

    st.subheader(
        "Incident Details"
    )

    pr_id = st.selectbox(
        "Select PR",
        incidents["PR_ID"].tolist()
    )

    incident = get_incident(
        pr_id
    )

    if incident is not None:

        st.write(
            "### Problem"
        )

        st.write(
            incident["Problem"]
        )

        st.write(
            "### Team Discussion"
        )

        st.info(
            incident["Discussion"]
        )

        st.write(
            "### Final Resolution"
        )

        st.success(
            incident["Final_Resolution"]
        )


# ============================================================
# GENERATE RUNBOOK
# ============================================================

elif page == "📘 Generate Runbook":

    st.title(
        "📘 Generate Maintenance Runbook"
    )

    st.write(
        """
        Select a completed pull request. The assistant combines
        the PR, incident, code diff and reviewer evidence.
        """
    )

    pr_id = st.selectbox(
        "Select Pull Request",
        pull_requests["PR_ID"].tolist()
    )

    if st.button(
        "🚀 Generate Runbook",
        type="primary"
    ):

        runbook = generate_runbook(
            pr_id
        )

        if runbook is not None:

            st.session_state.runbooks.append(
                runbook
            )

            db_save_runbook(runbook)

            add_audit(
                "Runbook Generated",
                f"Runbook generated for {pr_id}"
            )

            st.success(
                "Runbook generated successfully!"
            )

    if st.session_state.runbooks:

        runbook = (
            st.session_state.runbooks[-1]
        )

        st.divider()

        st.subheader(
            f"📘 Runbook: {runbook['PR_ID']}"
        )

        st.write(
            f"### {runbook['Title']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "### Problem"
            )

            st.write(
                runbook["Problem"]
            )

            st.write(
                "### Root Cause"
            )

            st.info(
                runbook["Root Cause"]
            )

            st.write(
                "### Solution"
            )

            st.success(
                runbook["Solution"]
            )

        with col2:

            st.write(
                "### Reviewer"
            )

            st.write(
                runbook["Reviewer"]
            )

            st.write(
                "### Reviewer Status"
            )

            if (
                runbook["Reviewer Status"]
                .lower()
                == "approved"
            ):

                st.success(
                    runbook["Reviewer Status"]
                )

            else:

                st.warning(
                    runbook["Reviewer Status"]
                )

            st.write(
                "### Verification"
            )

            if (
                runbook["Verification Status"]
                == "Verified"
            ):

                st.success(
                    runbook["Verification"]
                )

            else:

                st.warning(
                    runbook["Verification"]
                )

            st.write(
                "### Verification Status"
            )

            st.write(
                runbook["Verification Status"]
            )

            st.write(
                "### Confidence"
            )

            st.progress(
                runbook["Confidence"] / 100
            )

            st.write(
                f"{runbook['Confidence']}%"
            )

        # ============================================================
        # EVIDENCE BEHIND RECOMMENDATION
        # ============================================================

        st.divider()

        st.subheader(
            "🔎 Evidence Behind Recommendation"
        )

        st.write(
            """
            This section shows the evidence used by the assistant
            to generate and verify this maintenance runbook.
            """
        )

        evidence_col1, evidence_col2 = st.columns(2)

        # ------------------------------------------------------------
        # Pull Request Evidence
        # ------------------------------------------------------------

        with evidence_col1:

            st.write(
                "### 📋 Pull Request Evidence"
            )

            st.success(
                f"✓ {runbook['PR_ID']}"
            )

            st.write(
                f"**Title:** {runbook['Title']}"
            )

            st.write(
                f"**Resolution:** {runbook['Solution']}"
            )

        # ------------------------------------------------------------
        # Incident Evidence
        # ------------------------------------------------------------

        with evidence_col2:

            st.write(
                "### 🚨 Incident Evidence"
            )

            incident_evidence = get_incident(
                runbook["PR_ID"]
            )

            if incident_evidence is not None:

                st.success(
                    "✓ Incident discussion found"
                )

                st.write(
                    f"**Problem:** "
                    f"{incident_evidence['Problem']}"
                )

                st.write(
                    f"**Resolution:** "
                    f"{incident_evidence['Final_Resolution']}"
                )

            else:

                st.warning(
                    "⚠️ No incident evidence found"
                )

        # ------------------------------------------------------------
        # Code Diff Evidence
        # ------------------------------------------------------------

        st.write(
            "### 💻 Code Diff Evidence"
        )

        if (
            runbook["Changed File"]
            != "Code diff unavailable."
        ):

            st.success(
                "✓ Code diff found"
            )

            st.write(
                f"**Changed File:** "
                f"{runbook['Changed File']}"
            )

            diff_col1, diff_col2 = st.columns(2)

            with diff_col1:

                st.write(
                    "**Previous Code**"
                )

                st.code(
                    runbook["Old Code"]
                )

            with diff_col2:

                st.write(
                    "**Updated Code**"
                )

                st.code(
                    runbook["New Code"]
                )

        else:

            st.error(
                "❌ Code diff evidence is missing"
            )

        # ------------------------------------------------------------
        # Reviewer Evidence
        # ------------------------------------------------------------

        st.write(
            "### 👤 Reviewer Evidence"
        )

        reviewer_col1, reviewer_col2 = st.columns(2)

        with reviewer_col1:

            st.write(
                "**Reviewer:**"
            )

            st.write(
                runbook["Reviewer"]
            )

        with reviewer_col2:

            st.write(
                "**Reviewer Status:**"
            )

            if (
                runbook["Reviewer Status"]
                .lower()
                == "approved"
            ):

                st.success(
                    "✓ Approved"
                )

            else:

                st.warning(
                    runbook["Reviewer Status"]
                )

        # ------------------------------------------------------------
        # Evidence Completeness
        # ------------------------------------------------------------

        pr_evidence = True

        incident_evidence_available = (
            incident_evidence is not None
        )

        diff_evidence = (
            runbook["Changed File"]
            != "Code diff unavailable."
        )

        reviewer_evidence = (
            runbook["Reviewer Status"]
            .lower()
            == "approved"
        )

        evidence_count = sum(
            [
                pr_evidence,
                incident_evidence_available,
                diff_evidence,
                reviewer_evidence
            ]
        )

        st.divider()

        st.write(
            "### 📊 Evidence Completeness"
        )

        st.metric(
            "Verified Evidence Sources",
            f"{evidence_count} / 4"
        )

        if evidence_count == 4:

            st.success(
                "✅ All four required evidence sources are available."
            )

        elif evidence_count >= 2:

            st.warning(
                "⚠️ Some evidence is missing. "
                "Human review is recommended."
            )

        else:

            st.error(
                "❌ Insufficient evidence for a reliable recommendation."
            )

        # ------------------------------------------------------------
        # Why This Recommendation?
        # ------------------------------------------------------------

        st.write(
            "### 🧠 Why This Recommendation?"
        )

        if pr_evidence:

            st.write(
                "✓ The Pull Request contains the completed fix."
            )

        if incident_evidence_available:

            st.write(
                "✓ The Incident discussion explains the original problem."
            )

        if diff_evidence:

            st.write(
                "✓ The Code Diff confirms the actual implementation change."
            )

        if reviewer_evidence:

            st.write(
                "✓ A reviewer approved the proposed resolution."
            )

        st.write(
            f"**Final Confidence: "
            f"{runbook['Confidence']}%**"
        )

        st.divider()

        st.write(
            "### 🔧 Code Change"
        )

        st.write(
            f"**Changed File:** "
            f"{runbook['Changed File']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "Old Code"
            )

            st.code(
                runbook["Old Code"]
            )

        with col2:

            st.write(
                "New Code"
            )

            st.code(
                runbook["New Code"]
            )

        if runbook["High Impact"]:

            st.error(
                """
                🚨 HIGH-IMPACT CHANGE

                Human confirmation is required
                before approval.
                """
            )

        else:

            st.info(
                "This is classified as a normal-impact change."
            )


# ============================================================
# REVIEW RUNBOOKS
# ============================================================

elif page == "✅ Review Runbooks":

    st.title(
        "✅ Human Review"
    )

    if not st.session_state.runbooks:

        st.info(
            "Generate a runbook first."
        )

    else:

        for index, runbook in enumerate(
            st.session_state.runbooks
        ):

            st.divider()

            st.subheader(
                f"{runbook.get('PR_ID', '')} - "
                f"{runbook.get('Title', '')}"
            )

            st.write(
                f"Confidence: "
                f"**{runbook.get('Confidence', 0)}%**"
            )

            st.write(
                f"Verification: "
                f"**{runbook.get('Verification Status', 'Unknown')}**"
            )

            if (
                runbook.get("Changed File", "Code diff unavailable.")
                == "Code diff unavailable."
            ):

                st.error(
                    "❌ Approval blocked: Code diff is missing."
                )

                continue

            if (
                str(runbook.get("Reviewer Status", "")).lower()
                != "approved"
            ):

                st.warning(
                    "⏳ Approval blocked: Reviewer approval is required."
                )

                continue

            confirmation = True

            if runbook.get("High Impact", False):

                st.warning(
                    "⚠️ High-impact change detected."
                )

                confirmation = st.checkbox(
                    "I confirm that this high-impact runbook has been manually reviewed.",
                    key=f"confirm_{index}"
                )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Approve Runbook",
                    key=f"approve_{index}"
                ):

                    if not confirmation:

                        st.error(
                            "Human confirmation is required."
                        )

                    else:

                        if (
                            runbook["PR_ID"]
                            not in
                            st.session_state.approved_runbooks
                        ):

                            st.session_state.approved_runbooks.append(
                                runbook["PR_ID"]
                            )

                        runbook["Trust Status"] = "TRUSTED / VERIFIED"
                        db_save_runbook(runbook)

                        add_audit(
                            "Runbook Approved",
                            f"{runbook['PR_ID']} approved by human reviewer"
                        )

                        st.success(
                            "Runbook approved successfully."
                        )

            with col2:

                reject_reason = st.text_input(
                    "Rejection reason",
                    key=f"reason_{index}"
                )

                if st.button(
                    "❌ Reject Runbook",
                    key=f"reject_{index}"
                ):

                    if not reject_reason.strip():

                        st.error(
                            "Please provide a rejection reason."
                        )

                    else:

                        add_audit(
                            "Runbook Rejected",
                            f"{runbook['PR_ID']}: {reject_reason}"
                        )

                        st.warning(
                            "Runbook rejected."
                        )

    if st.session_state.approved_runbooks:

        st.divider()

        st.subheader(
            "✅ Approved Runbooks"
        )

        for item in (
            st.session_state.approved_runbooks
        ):

            st.success(
                item
            )


# ============================================================
# API INTEGRATION
# ============================================================

elif page == "🔌 API Integration":

    st.title(
        "🔌 API Integration"
    )

    st.write(
        """
        A production version could connect with GitHub, GitLab,
        Jira or incident-management systems.

        This prototype uses a Mock API to demonstrate the integration.
        """
    )

    st.info(
        "🔌 Mock API — no production system is modified."
    )

    pr_id = st.selectbox(
        "Select PR",
        pull_requests["PR_ID"].tolist()
    )

    if st.button(
        "📡 Send Data to Mock API",
        type="primary"
    ):

        payload = mock_api_send(
            pr_id
        )

        st.success(
            "Data successfully received by Mock API."
        )

        st.json(
            payload
        )

    if st.session_state.api_records:

        st.divider()

        st.subheader(
            "API Activity"
        )

        st.metric(
            "API Calls",
            len(
                st.session_state.api_records
            )
        )


# ============================================================
# ROLLBACK MANAGER
# ============================================================

elif page == "🔄 Rollback Manager":

    st.title(
        "🔄 Rollback Manager"
    )

    st.warning(
        """
        Prototype simulation only.

        This feature does NOT modify production code.
        It records the rollback path and reason.
        """
    )

    pr_id = st.selectbox(
        "Select Pull Request",
        pull_requests["PR_ID"].tolist()
    )

    pr = get_pr(pr_id)

    diff = get_diff(pr_id)

    if pr is not None:

        st.subheader(
            f"{pr_id} - {pr['Title']}"
        )

        if diff is not None:

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "### Previous Version"
                )

                st.code(
                    str(diff["Old_Code"])
                )

            with col2:

                st.write(
                    "### Current Version"
                )

                st.code(
                    str(diff["New_Code"])
                )

        combined_text = (
            str(pr["Title"])
            + " "
            + str(pr["Description"])
            + " "
            + str(pr["Resolution"])
        )

        high_impact = is_high_impact(
            combined_text
        )

        if high_impact:

            st.error(
                "🚨 High-impact change. Human confirmation required."
            )

            rollback_confirmation = st.checkbox(
                "I confirm that rollback is required."
            )

        else:

            rollback_confirmation = True

        reason = st.text_area(
            "Rollback Reason",
            placeholder="Explain why the rollback is required..."
        )

        if st.button(
            "🔄 Record Rollback",
            type="primary"
        ):

            if not rollback_confirmation:

                st.error(
                    "Human confirmation is required."
                )

            elif not reason.strip():

                st.error(
                    "Rollback reason is required."
                )

            else:

                record = {

                    "PR_ID":
                        pr_id,

                    "Reason":
                        reason,

                    "Timestamp":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                    "Status":
                        "Rollback Path Recorded"
                }

                st.session_state.rollback_log.append(
                    record
                )

                db_save_rollback(record)

                add_audit(
                    "Rollback Recorded",
                    f"{pr_id}: {reason}"
                )

                st.success(
                    "Rollback path recorded successfully."
                )

    if st.session_state.rollback_log:

        st.divider()

        st.subheader(
            "🔄 Rollback History"
        )

        st.dataframe(
            pd.DataFrame(
                st.session_state.rollback_log
            ),
            use_container_width=True
        )


# ============================================================
# RISK CHECKER
# ============================================================

elif page == "⚠️ Risk Checker":

    st.title(
        "⚠️ Risk Checker"
    )

    st.write(
        """
        The prototype uses rule-based detection to identify
        potentially high-impact maintenance changes.
        """
    )

    st.info(
        """
        High-impact keywords:

        authentication • security • password • permission •
        database • payment • delete • production •
        credential • access
        """
    )

    pr_id = st.selectbox(
        "Select Pull Request",
        pull_requests["PR_ID"].tolist()
    )

    pr = get_pr(pr_id)

    if pr is not None:

        combined_text = (
            str(pr["Title"])
            + " "
            + str(pr["Description"])
            + " "
            + str(pr["Resolution"])
        )

        high_impact = is_high_impact(
            combined_text
        )

        st.subheader(
            f"Risk Result — {pr_id}"
        )

        if high_impact:

            st.error(
                "🚨 HIGH-IMPACT CHANGE"
            )

            st.write(
                """
                Human confirmation is required before
                this change can become trusted maintenance knowledge.
                """
            )

        else:

            st.success(
                "✅ NORMAL-IMPACT CHANGE"
            )

            st.write(
                "Standard human review can be followed."
            )


# ============================================================
# EDGE CASES
# ============================================================

elif page == "🧪 Edge Cases":

    st.title(
        "🧪 Edge & Failure Cases"
    )

    st.write(
        """
        These cases demonstrate how the assistant behaves when
        evidence is missing, review is incomplete, or a risky
        action is detected.
        """
    )

    cases = [

        {
            "Case":
                "Missing Incident",

            "Condition":
                "Incident record does not exist",

            "System Response":
                "Show warning and mark root-cause evidence incomplete."
        },

        {
            "Case":
                "Pending Reviewer",

            "Condition":
                "Reviewer has not approved the fix",

            "System Response":
                "Block runbook approval."
        },

        {
            "Case":
                "Missing Code Diff",

            "Condition":
                "No code change evidence is available",

            "System Response":
                "Mark runbook incomplete."
        },

        {
            "Case":
                "High-Impact Change",

            "Condition":
                "Security/authentication/database/production keyword detected",

            "System Response":
                "Require human confirmation."
        },

        {
            "Case":
                "Rollback Without Reason",

            "Condition":
                "Rollback is attempted without explanation",

            "System Response":
                "Block rollback recording."
        }
    ]

    edge_df = pd.DataFrame(
        cases
    )

    st.dataframe(
        edge_df,
        use_container_width=True
    )

    st.subheader(
        "🧪 Test an Edge Case"
    )

    test_case = st.selectbox(
        "Choose Edge Case",
        [
            "Missing Incident",
            "Pending Reviewer",
            "Missing Code Diff",
            "High-Impact Change",
            "Rollback Without Reason"
        ]
    )

    if test_case == "Missing Incident":

        st.warning(
            "⚠️ Incident information unavailable."
        )

    elif test_case == "Pending Reviewer":

        st.warning(
            "⏳ Approval blocked until reviewer approval."
        )

    elif test_case == "Missing Code Diff":

        st.error(
            "❌ Runbook marked incomplete."
        )

    elif test_case == "High-Impact Change":

        st.error(
            "🚨 Human confirmation required."
        )

    elif test_case == "Rollback Without Reason":

        st.error(
            "❌ Rollback blocked because a reason is required."
        )


# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "📝 Audit Trail":

    st.title(
        "📝 Audit Trail"
    )

    st.write(
        """
        The audit trail records important system actions,
        including runbook generation, approval, rejection,
        API reception and rollback.
        """
    )

    if not st.session_state.audit_log:

        st.info(
            "No audit events yet."
        )

    else:

        audit_df = pd.DataFrame(
            st.session_state.audit_log
        )

        st.dataframe(
            audit_df,
            use_container_width=True
        )

        st.subheader(
            "📊 Audit Summary"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Events",
                len(audit_df)
            )

        with col2:

            st.metric(
                "Runbooks Generated",
                sum(
                    audit_df["Action"]
                    == "Runbook Generated"
                )
            )

        with col3:

            st.metric(
                "Approvals",
                sum(
                    audit_df["Action"]
                    == "Runbook Approved"
                )
            )


# ============================================================
# VALIDATION DASHBOARD
# ============================================================

elif page == "📊 Validation Dashboard":

    st.title("📊 Validation Dashboard")

    st.write(
        """
        Measure whether the assistant reduces the time required for a new
        engineer to repeat a known maintenance fix. All validation runs in
        this prototype are synthetic or simulated unless explicitly stated.
        """
    )

    # --------------------------------------------------------
    # MANAGE EXISTING RESULTS
    # --------------------------------------------------------

    if st.session_state.experiment_results:

        st.subheader("🗑️ Manage Validation Results")

        validation_options = []
        validation_lookup = {}

        for idx, row in enumerate(st.session_state.experiment_results):
            validation_id = row.get("Validation ID")
            label = (
                f"{validation_id if validation_id is not None else idx + 1} — "
                f"{row.get('Test Case', 'Unknown')} — "
                f"Baseline {float(row.get('Baseline Minutes', 0)):.1f} / "
                f"Assistant {float(row.get('Assistant Minutes', 0)):.1f}"
            )
            validation_options.append(label)
            validation_lookup[label] = (idx, validation_id)

        selected_validation = st.selectbox(
            "Select a result to remove",
            validation_options,
            key="validation_delete_select"
        )

        if st.button("🗑️ Delete Selected Result"):

            selected_idx, validation_id = validation_lookup[selected_validation]
            selected_row = st.session_state.experiment_results[selected_idx]

            if validation_id is not None:
                db_delete_validation(validation_id)

            st.session_state.experiment_results.pop(selected_idx)

            add_audit(
                "Validation Result Deleted",
                f"Deleted validation result: {selected_row.get('Test Case', 'Unknown')}"
            )

            st.success("Validation result deleted successfully.")
            st.rerun()

    st.subheader("➕ Add Experiment Result")

    col1, col2 = st.columns(2)

    with col1:

        test_case = st.text_input(
            "Test Case",
            placeholder="Example: PR102 - Database connection retry"
        )

        baseline_time = st.number_input(
            "Baseline Time (minutes)",
            min_value=1.0,
            value=60.0,
            step=1.0
        )

        tester_id = st.text_input(
            "Tester / Simulated Engineer ID",
            placeholder="Example: Engineer-01"
        )

    with col2:

        assistant_time = st.number_input(
            "With Assistant (minutes)",
            min_value=1.0,
            value=30.0,
            step=1.0
        )

        result = st.selectbox(
            "Result",
            [
                "Success",
                "Partial Success",
                "Failure"
            ]
        )

        correctness = st.selectbox(
            "Recommendation Correctness",
            [
                "Correct",
                "Partially Correct",
                "Incorrect",
                "Not Recorded"
            ]
        )

    observation = st.text_area(
        "Observation / Error Analysis",
        placeholder="Describe what happened during the test..."
    )

    if st.button("➕ Add Result", type="primary"):

        clean_case = test_case.strip()
        clean_tester = tester_id.strip() or "Not Recorded"
        clean_observation = observation.strip()

        if not clean_case:

            st.error("Please enter a test case.")

        elif assistant_time > baseline_time and result == "Success":

            st.error(
                "The assistant was slower than baseline, so Result cannot be Success. "
                "Use Partial Success or Failure and explain the regression in Error Analysis."
            )

        elif assistant_time > baseline_time and not clean_observation:

            st.error(
                "A slower-than-baseline run requires an observation explaining the regression."
            )

        else:

            time_saved = baseline_time - assistant_time
            reduction = (time_saved / baseline_time) * 100

            experiment = {
                "Validation ID": None,
                "Test Case": clean_case,
                "Tester ID": clean_tester,
                "Baseline Minutes": float(baseline_time),
                "Assistant Minutes": float(assistant_time),
                "Time Saved": float(time_saved),
                "Reduction %": float(reduction),
                "Result": result,
                "Recommendation Correctness": correctness,
                "Observation": clean_observation,
                "Created At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            db_save_validation(experiment)

            # Read back the generated SQLite ID so the delete control can
            # target the exact persistent record.
            conn = get_db_connection()
            row_id = conn.execute(
                "SELECT id FROM validation_results ORDER BY id DESC LIMIT 1"
            ).fetchone()
            conn.close()

            if row_id:
                experiment["Validation ID"] = row_id[0]

            st.session_state.experiment_results.append(experiment)

            add_audit(
                "Validation Result Added",
                clean_case
            )

            st.success("Validation result added successfully.")
            st.rerun()

    # --------------------------------------------------------
    # DISPLAY VALIDATION RESULTS
    # --------------------------------------------------------

    if st.session_state.experiment_results:

        results_df = pd.DataFrame(st.session_state.experiment_results)

        st.divider()
        st.subheader("📈 Experiment Metrics")

        avg_baseline = results_df["Baseline Minutes"].mean()
        avg_assistant = results_df["Assistant Minutes"].mean()
        avg_saved = results_df["Time Saved"].mean()
        avg_reduction = results_df["Reduction %"].mean()
        median_reduction = results_df["Reduction %"].median()
        std_reduction = results_df["Reduction %"].std(ddof=1) if len(results_df) > 1 else 0.0
        success_rate = (results_df["Result"] == "Success").mean() * 100

        correctness_recorded = results_df[
            results_df["Recommendation Correctness"].isin(
                ["Correct", "Partially Correct", "Incorrect"]
            )
        ]
        correctness_rate = (
            (correctness_recorded["Recommendation Correctness"] == "Correct").mean() * 100
            if not correctness_recorded.empty else 0.0
        )

        regression_count = int((results_df["Reduction %"] < 0).sum())

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Avg Baseline", f"{avg_baseline:.1f} min")

        with col2:
            st.metric("Avg Assistant", f"{avg_assistant:.1f} min")

        with col3:
            st.metric("Avg Time Saved", f"{avg_saved:.1f} min")

        with col4:
            st.metric("Avg Reduction", f"{avg_reduction:.1f}%")

        with col5:
            st.metric("Success Rate", f"{success_rate:.1f}%")

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric("Median Reduction", f"{median_reduction:.1f}%")

        with metric_col2:
            st.metric("Reduction Std Dev", f"{std_reduction:.1f}%")

        with metric_col3:
            st.metric("Regression Cases", regression_count)

        if not correctness_recorded.empty:
            st.metric("Correctness Rate", f"{correctness_rate:.1f}%")
        else:
            st.info("Recommendation correctness has not been recorded for any run yet.")

        # ----------------------------------------------------
        # TARGET
        # ----------------------------------------------------

        target = 30

        st.subheader("🎯 Target")

        if avg_reduction >= target:
            st.success(
                f"Target achieved!\n\n"
                f"Target: {target}% reduction\n\n"
                f"Measured: {avg_reduction:.1f}% reduction"
            )
        else:
            st.warning(
                f"Target not yet achieved.\n\n"
                f"Target: {target}% reduction\n\n"
                f"Measured: {avg_reduction:.1f}% reduction"
            )

        # ----------------------------------------------------
        # RESULTS TABLE
        # ----------------------------------------------------

        st.subheader("📋 Experiment Results")
        st.dataframe(results_df, use_container_width=True)

        # ----------------------------------------------------
        # TIME COMPARISON
        # ----------------------------------------------------

        st.subheader("⏱️ Time Comparison")

        for _, row in results_df.iterrows():

            st.write(f"**{row['Test Case']}**")

            baseline = float(row["Baseline Minutes"])
            assistant = float(row["Assistant Minutes"])
            percentage = int(min(max((assistant / baseline) * 100, 0), 100))

            st.write(f"Baseline: {baseline:.1f} minutes")
            st.progress(100)
            st.write(f"Assistant: {assistant:.1f} minutes")
            st.progress(percentage)
            st.write(
                f"Time saved: {row['Time Saved']:.1f} minutes "
                f"({row['Reduction %']:.1f}%)"
            )
            st.divider()

        # ----------------------------------------------------
        # ERROR / REGRESSION ANALYSIS
        # ----------------------------------------------------

        st.subheader("🔍 Error Analysis")

        problems = results_df[
            (results_df["Result"] != "Success")
            | (results_df["Reduction %"] < 0)
            | (results_df["Recommendation Correctness"] == "Incorrect")
        ]

        if problems.empty:
            st.success("No failed, partial, or regression validation cases recorded.")
        else:
            st.warning(
                f"{len(problems)} validation case(s) need further analysis."
            )
            st.dataframe(
                problems[
                    [
                        "Test Case",
                        "Tester ID",
                        "Result",
                        "Reduction %",
                        "Recommendation Correctness",
                        "Observation"
                    ]
                ],
                use_container_width=True
            )

    else:
        st.info("Add experiment results to display validation metrics.")


# ============================================================
# END
# ============================================================
