import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import sqlite3
import json
import re
import statistics


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
# PROJECT PATHS AND PERSISTENT STORAGE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "maintenance_assistant.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS runbooks (
        pr_id TEXT PRIMARY KEY, payload_json TEXT NOT NULL,
        trust_status TEXT NOT NULL, human_reviewer TEXT DEFAULT '',
        approval_reason TEXT DEFAULT '', rejection_reason TEXT DEFAULT '',
        created_at TEXT NOT NULL, updated_at TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL,
        action TEXT NOT NULL, details TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS rollback_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT, pr_id TEXT NOT NULL,
        reason TEXT NOT NULL, timestamp TEXT NOT NULL, status TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS validation_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT, tester_id TEXT NOT NULL,
        test_case TEXT NOT NULL, baseline_minutes REAL NOT NULL,
        assistant_minutes REAL NOT NULL, time_saved REAL NOT NULL,
        reduction_pct REAL NOT NULL, result TEXT NOT NULL,
        correctness TEXT NOT NULL, observation TEXT DEFAULT '', timestamp TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()


init_db()


def db_runbook_rows():
    with get_db() as conn:
        return conn.execute("SELECT * FROM runbooks ORDER BY updated_at DESC").fetchall()


def db_audit_rows():
    with get_db() as conn:
        return conn.execute("SELECT timestamp AS Timestamp, action AS Action, details AS Details FROM audit_log ORDER BY id").fetchall()


def db_rollback_rows():
    with get_db() as conn:
        return conn.execute("SELECT pr_id AS PR_ID, reason AS Reason, timestamp AS Timestamp, status AS Status FROM rollback_log ORDER BY id").fetchall()


def db_validation_rows():
    with get_db() as conn:
        return conn.execute("SELECT * FROM validation_results ORDER BY id").fetchall()


def persist_runbook(runbook):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db() as conn:
        conn.execute("""INSERT INTO runbooks
            (pr_id, payload_json, trust_status, human_reviewer, approval_reason, rejection_reason, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(pr_id) DO UPDATE SET
            payload_json=excluded.payload_json, trust_status=excluded.trust_status,
            human_reviewer=excluded.human_reviewer, approval_reason=excluded.approval_reason,
            rejection_reason=excluded.rejection_reason, updated_at=excluded.updated_at""",
            (runbook["PR_ID"], json.dumps(runbook), runbook.get("Trust Status", "PENDING HUMAN APPROVAL"),
             runbook.get("Human Reviewer", ""), runbook.get("Approval Reason", ""),
             runbook.get("Rejection Reason", ""), runbook.get("Created At", now), now))


def update_trust(pr_id, status, reviewer="", approval_reason="", rejection_reason=""):
    rows = db_runbook_rows()
    payload = None
    for row in rows:
        if row["pr_id"] == pr_id:
            payload = json.loads(row["payload_json"])
            break
    if payload is None:
        return None
    payload["Trust Status"] = status
    payload["Human Reviewer"] = reviewer
    payload["Approval Reason"] = approval_reason
    payload["Rejection Reason"] = rejection_reason
    payload["Updated At"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    persist_runbook(payload)
    return payload


def persist_rollback(record):
    with get_db() as conn:
        conn.execute("INSERT INTO rollback_log (pr_id, reason, timestamp, status) VALUES (?, ?, ?, ?)",
                     (record["PR_ID"], record["Reason"], record["Timestamp"], record["Status"]))


def persist_validation(record):
    with get_db() as conn:
        conn.execute("""INSERT INTO validation_results
            (tester_id, test_case, baseline_minutes, assistant_minutes, time_saved, reduction_pct, result, correctness, observation, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (record["Tester ID"], record["Test Case"], record["Baseline Minutes"], record["Assistant Minutes"],
             record["Time Saved"], record["Reduction %"], record["Result"], record["Correctness"],
             record["Observation"], record["Timestamp"]))


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
# SESSION STATE
# ============================================================

if "runbooks" not in st.session_state:
    st.session_state.runbooks = [json.loads(r["payload_json"]) for r in db_runbook_rows()]

if "audit_log" not in st.session_state:
    st.session_state.audit_log = [dict(r) for r in db_audit_rows()]

if "api_records" not in st.session_state:
    st.session_state.api_records = []

if "rollback_log" not in st.session_state:
    st.session_state.rollback_log = [dict(r) for r in db_rollback_rows()]

if "experiment_results" not in st.session_state:
    st.session_state.experiment_results = [dict(r) for r in db_validation_rows()]

if "approved_runbooks" not in st.session_state:
    st.session_state.approved_runbooks = [
        r["pr_id"] for r in db_runbook_rows() if r["trust_status"] == "TRUSTED / VERIFIED"
    ]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def add_audit(action, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {"Timestamp": timestamp, "Action": action, "Details": details}
    st.session_state.audit_log.append(record)
    with get_db() as conn:
        conn.execute("INSERT INTO audit_log (timestamp, action, details) VALUES (?, ?, ?)",
                     (timestamp, action, details))


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
# STRUCTURED EXTRACTION
# ============================================================

def split_sentences(text):
    text = str(text or "").strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+|\n+|\s*;\s*", text)
    return [p.strip(" -•") for p in parts if p.strip(" -•")]


def extract_root_cause_signals(text):
    sentences = split_sentences(text)
    keywords = [
        "because", "caused", "root cause", "due to", "failure",
        "timeout", "missing", "misconfigured", "incorrect", "error",
        "exception", "bug", "issue", "dependency"
    ]
    matches = [s for s in sentences if any(k in s.lower() for k in keywords)]
    return matches[:3] if matches else sentences[:2]


def extract_action_steps(text):
    sentences = split_sentences(text)
    action_words = [
        "update", "change", "replace", "add", "remove", "configure",
        "set", "modify", "fix", "restart", "deploy", "install", "enable", "disable"
    ]
    matches = [s for s in sentences if any(k in s.lower() for k in action_words)]
    return matches[:5] if matches else sentences[:3]


def extract_verification_steps(text):
    sentences = split_sentences(text)
    verification_words = [
        "verify", "test", "tested", "check", "confirmed", "pass",
        "passed", "validate", "validation", "working", "monitor"
    ]
    matches = [s for s in sentences if any(k in s.lower() for k in verification_words)]
    return matches[:4]


def evidence_summary(pr, incident, diff, review):
    sources = ["Pull Request"]
    if incident is not None:
        sources.append("Incident Discussion")
    if diff is not None:
        sources.append("Code Diff")
    if review is not None and str(review["Decision"]).lower() == "approved":
        sources.append("Approved Review")
    return sources


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

        discussion = ""
        root_cause_signals = []
        problem = str(pr["Description"])
        root_cause = "Incident information unavailable."
        incident_resolution = "Not available."

    else:

        problem = str(
            incident["Problem"]
        )

        discussion = str(incident["Discussion"])
        root_cause_signals = extract_root_cause_signals(discussion)
        root_cause = (
            root_cause_signals[0] if root_cause_signals
            else "Root cause could not be extracted from the discussion."
        )
        incident_resolution = str(incident["Final_Resolution"])

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

        "Root Cause Signals":
            root_cause_signals,

        "Action Steps":
            extract_action_steps(str(pr["Resolution"])),

        "Verification Steps":
            extract_verification_steps(str(review["Comment"]) if review is not None else ""),

        "Evidence Sources":
            evidence_summary(pr, incident, diff, review),

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

        "Human Reviewer":
            "",

        "Approval Reason":
            "",

        "Rejection Reason":
            "",

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

            # Replace an existing runbook for the same PR instead of creating duplicates.
            st.session_state.runbooks = [
                r for r in st.session_state.runbooks if r.get("PR_ID") != pr_id
            ]
            st.session_state.runbooks.append(runbook)
            persist_runbook(runbook)

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

            st.write("### Extracted Root-Cause Signals")
            if runbook.get("Root Cause Signals"):
                for signal in runbook["Root Cause Signals"]:
                    st.write(f"• {signal}")
            else:
                st.write("No strong root-cause signal extracted.")

            st.write("### Reusable Action Steps")
            for step_no, step in enumerate(runbook.get("Action Steps", []), 1):
                st.write(f"{step_no}. {step}")

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

            st.write("### Verification Steps Extracted")
            verification_steps = runbook.get("Verification Steps", [])
            if verification_steps:
                for step_no, step in enumerate(verification_steps, 1):
                    st.write(f"{step_no}. {step}")
            else:
                st.info("No explicit verification sentence was found in the reviewer evidence.")

            st.write("### Evidence Sources")
            st.write(" → ".join(runbook.get("Evidence Sources", [])))

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

    st.title("✅ Human Review & Trust Management")
    st.write("A runbook becomes trusted only after explicit human approval. The trust state is stored in SQLite.")

    if not st.session_state.runbooks:
        st.info("Generate a runbook first.")
    else:
        for index, runbook in enumerate(st.session_state.runbooks):
            st.divider()
            pr_id = runbook["PR_ID"]
            st.subheader(f"{pr_id} - {runbook['Title']}")
            st.write(f"**Current Trust Status:** {runbook.get('Trust Status', 'PENDING HUMAN APPROVAL')}")
            st.write(f"**Verification:** {runbook['Verification Status']}")

            if runbook["Changed File"] == "Code diff unavailable.":
                st.error("❌ Approval blocked: Code diff is missing.")
                continue

            if runbook["Reviewer Status"].lower() != "approved":
                st.warning("⏳ Approval blocked: Source reviewer approval is required.")
                continue

            reviewer_name = st.text_input("Human reviewer name", key=f"reviewer_{index}")
            approval_reason = st.text_area("Approval / review reason", key=f"approval_reason_{index}",
                                           placeholder="Explain why this runbook is reliable and reusable...")

            confirmation = True
            if runbook["High Impact"]:
                st.warning("⚠️ High-impact change detected. Additional confirmation is required.")
                confirmation = st.checkbox("I confirm that I manually reviewed this high-impact runbook.", key=f"confirm_{index}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve as Trusted Knowledge", key=f"approve_{index}"):
                    if not reviewer_name.strip():
                        st.error("Enter the human reviewer name.")
                    elif not approval_reason.strip():
                        st.error("Provide an approval reason.")
                    elif not confirmation:
                        st.error("Human confirmation is required for this high-impact runbook.")
                    else:
                        updated = update_trust(pr_id, "TRUSTED / VERIFIED", reviewer_name.strip(), approval_reason.strip())
                        st.session_state.runbooks[index] = updated
                        if pr_id not in st.session_state.approved_runbooks:
                            st.session_state.approved_runbooks.append(pr_id)
                        add_audit("Runbook Trusted", f"{pr_id} trusted by {reviewer_name.strip()}: {approval_reason.strip()}")
                        st.success("Runbook is now TRUSTED / VERIFIED and persisted.")

            with col2:
                reject_reason = st.text_area("Rejection reason", key=f"reason_{index}")
                if st.button("❌ Reject Runbook", key=f"reject_{index}"):
                    if not reject_reason.strip():
                        st.error("Please provide a rejection reason.")
                    else:
                        updated = update_trust(pr_id, "REJECTED", reviewer_name.strip(), rejection_reason=reject_reason.strip())
                        st.session_state.runbooks[index] = updated
                        if pr_id in st.session_state.approved_runbooks:
                            st.session_state.approved_runbooks.remove(pr_id)
                        add_audit("Runbook Rejected", f"{pr_id}: {reject_reason.strip()}")
                        st.warning("Runbook rejected and the decision was persisted.")

            if runbook.get("Trust Status") == "TRUSTED / VERIFIED":
                st.success(f"Trusted by {runbook.get('Human Reviewer', 'Unknown reviewer')}")
                revoke_reason = st.text_input("Reason to revoke (if needed)", key=f"revoke_reason_{index}")
                if st.button("↩️ Revoke Trust", key=f"revoke_{index}"):
                    if not revoke_reason.strip():
                        st.error("A revocation reason is required.")
                    else:
                        updated = update_trust(pr_id, "REVOKED", runbook.get("Human Reviewer", ""), rejection_reason=revoke_reason.strip())
                        st.session_state.runbooks[index] = updated
                        if pr_id in st.session_state.approved_runbooks:
                            st.session_state.approved_runbooks.remove(pr_id)
                        add_audit("Runbook Trust Revoked", f"{pr_id}: {revoke_reason.strip()}")
                        st.warning("Trust revoked and persisted.")

    if st.session_state.approved_runbooks:
        st.divider()
        st.subheader("✅ Trusted Runbooks")
        st.write(", ".join(st.session_state.approved_runbooks))


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

    st.title("🔄 Rollback Manager")
    st.warning("Prototype simulation only. No production code is modified.")

    pr_id = st.selectbox("Select Pull Request", pull_requests["PR_ID"].tolist())
    pr = get_pr(pr_id)
    diff = get_diff(pr_id)

    if pr is not None:
        st.subheader(f"{pr_id} - {pr['Title']}")
        if diff is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Previous Version")
                st.code(str(diff["Old_Code"]))
            with col2:
                st.write("### Current Version")
                st.code(str(diff["New_Code"]))

        combined_text = str(pr["Title"]) + " " + str(pr["Description"]) + " " + str(pr["Resolution"])
        high_impact = is_high_impact(combined_text)
        rollback_confirmation = True
        if high_impact:
            st.error("🚨 High-impact change. Human confirmation required.")
            rollback_confirmation = st.checkbox("I confirm that rollback is required.")

        reason = st.text_area("Rollback Reason", placeholder="Explain why the rollback is required...")
        if st.button("🔄 Record Rollback", type="primary"):
            if not rollback_confirmation:
                st.error("Human confirmation is required.")
            elif not reason.strip():
                st.error("Rollback reason is required.")
            else:
                record = {"PR_ID": pr_id, "Reason": reason.strip(),
                          "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          "Status": "Rollback Path Recorded"}
                st.session_state.rollback_log.append(record)
                persist_rollback(record)
                add_audit("Rollback Recorded", f"{pr_id}: {reason.strip()}")
                st.success("Rollback path recorded and persisted successfully.")

    if st.session_state.rollback_log:
        st.divider()
        st.subheader("🔄 Rollback History")
        st.dataframe(pd.DataFrame(st.session_state.rollback_log), use_container_width=True)


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
    st.write("Measure whether the assistant reduces the time required for a new engineer to repeat a known maintenance fix.")

    st.subheader("➕ Add Experiment Result")
    col1, col2 = st.columns(2)
    with col1:
        tester_id = st.text_input("Tester / Engineer ID", placeholder="Engineer-01")
        test_case = st.text_input("Test Case", placeholder="Example: Redis timeout fix")
        baseline_time = st.number_input("Baseline Time (minutes)", min_value=0.1, value=60.0)
    with col2:
        assistant_time = st.number_input("With Assistant (minutes)", min_value=0.1, value=30.0)
        result = st.selectbox("Result", ["Success", "Partial Success", "Failure"])
        correctness = st.selectbox("Recommendation Correctness", ["Correct", "Partially Correct", "Incorrect", "Not Assessed"])

    observation = st.text_area("Observation / Error Analysis", placeholder="Record errors, missing evidence, wrong steps, or what made the run successful...")

    if st.button("➕ Add Result", type="primary"):
        if not tester_id.strip() or not test_case.strip():
            st.error("Tester / Engineer ID and Test Case are required.")
        else:
            time_saved = baseline_time - assistant_time
            reduction = (time_saved / baseline_time) * 100
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            experiment = {
                "Tester ID": tester_id.strip(),
                "Test Case": test_case.strip(),
                "Baseline Minutes": float(baseline_time),
                "Assistant Minutes": float(assistant_time),
                "Time Saved": float(time_saved),
                "Reduction %": float(reduction),
                "Result": result,
                "Correctness": correctness,
                "Observation": observation.strip(),
                "Timestamp": timestamp
            }
            st.session_state.experiment_results.append(experiment)
            persist_validation(experiment)
            add_audit("Validation Result Added", f"{test_case.strip()} by {tester_id.strip()}")
            st.success("Validation result saved permanently.")

    if st.session_state.experiment_results:
        results_df = pd.DataFrame(st.session_state.experiment_results)
        st.divider()
        st.subheader("📈 Experiment Metrics")

        baselines = results_df["Baseline Minutes"].astype(float).tolist()
        assistants = results_df["Assistant Minutes"].astype(float).tolist()
        reductions = results_df["Reduction %"].astype(float).tolist()
        saved = results_df["Time Saved"].astype(float).tolist()
        avg_baseline = statistics.mean(baselines)
        avg_assistant = statistics.mean(assistants)
        avg_saved = statistics.mean(saved)
        avg_reduction = statistics.mean(reductions)
        median_reduction = statistics.median(reductions)
        std_reduction = statistics.stdev(reductions) if len(reductions) > 1 else 0.0
        success_rate = (results_df["Result"] == "Success").mean() * 100
        correctness_rate = (results_df["Correctness"] == "Correct").mean() * 100
        regression_count = int((results_df["Assistant Minutes"] > results_df["Baseline Minutes"]).sum())
        target = 30.0

        metrics = st.columns(6)
        metrics[0].metric("Avg Baseline", f"{avg_baseline:.1f} min")
        metrics[1].metric("Avg Assistant", f"{avg_assistant:.1f} min")
        metrics[2].metric("Avg Saved", f"{avg_saved:.1f} min")
        metrics[3].metric("Avg Reduction", f"{avg_reduction:.1f}%")
        metrics[4].metric("Success Rate", f"{success_rate:.1f}%")
        metrics[5].metric("Correctness", f"{correctness_rate:.1f}%")

        st.subheader("🎯 Evaluation Target")
        st.write(f"Target reduction: **{target:.0f}%**")
        st.write(f"Measured average reduction: **{avg_reduction:.1f}%**")
        if avg_reduction >= target:
            st.success("Target achieved in the currently recorded test data.")
        else:
            st.warning("Target not yet achieved in the currently recorded test data.")

        st.subheader("📊 Statistical Summary")
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        stat_col1.metric("Median Reduction", f"{median_reduction:.1f}%")
        stat_col2.metric("Std. Dev. of Reduction", f"{std_reduction:.1f}%")
        stat_col3.metric("Regression Cases", str(regression_count))
        st.caption("Regression cases are retained intentionally: the assistant is not forced to look faster than baseline.")

        st.subheader("📋 Experiment Results")
        st.dataframe(results_df, use_container_width=True)

        st.subheader("🔍 Error Analysis")
        non_success = results_df[results_df["Result"] != "Success"]
        incorrect = results_df[results_df["Correctness"].isin(["Partially Correct", "Incorrect"])]
        if non_success.empty and incorrect.empty and regression_count == 0:
            st.success("No failures, incorrect recommendations, or regressions recorded yet.")
        else:
            st.write(f"**Non-success cases:** {len(non_success)}")
            st.write(f"**Partially correct / incorrect recommendations:** {len(incorrect)}")
            st.write(f"**Regression cases:** {regression_count}")
            analysis_df = pd.concat([non_success, incorrect]).drop_duplicates(subset=["Tester ID", "Test Case", "Timestamp"])
            if not analysis_df.empty:
                st.dataframe(analysis_df[["Tester ID", "Test Case", "Result", "Correctness", "Baseline Minutes", "Assistant Minutes", "Reduction %", "Observation"]], use_container_width=True)

        st.subheader("👥 Tester Coverage")
        st.write(f"Unique testers: **{results_df['Tester ID'].nunique()}**")
        st.write(f"Test cases recorded: **{len(results_df)}**")
    else:
        st.info("Add experiment results to display validation metrics.")


# ============================================================
# END
# ============================================================
