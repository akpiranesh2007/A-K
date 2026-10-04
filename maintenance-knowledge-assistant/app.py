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
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Prototype persistence files. These keep audit/trust state during
# the Streamlit runtime and make the state visible in the data folder.
AUDIT_FILE = DATA_DIR / "audit_log.csv"
TRUST_FILE = DATA_DIR / "trusted_runbooks.csv"
ROLLBACK_FILE = DATA_DIR / "rollback_log.csv"
EXPERIMENT_FILE = DATA_DIR / "experiment_results.csv"
SQLITE_FILE = DATA_DIR / "maintenance_assistant.db"


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

    # Keep identifiers consistent even when CSV readers infer different types.
    for df in (pull_requests, incidents, code_diffs, reviews):
        if "PR_ID" in df.columns:
            df["PR_ID"] = df["PR_ID"].astype(str)

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

if "change_review_log" not in st.session_state:
    st.session_state.change_review_log = []

if "trusted_metadata" not in st.session_state:
    st.session_state.trusted_metadata = {}

if "human_confirmations" not in st.session_state:
    st.session_state.human_confirmations = []

if "persistence_loaded" not in st.session_state:
    st.session_state.persistence_loaded = False

if "persistence_warning" not in st.session_state:
    st.session_state.persistence_warning = ""


# ============================================================
# PERSISTENCE + TRUST HELPERS
# ============================================================

def _db_connect():
    """Open the durable SQLite store used by the prototype."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(SQLITE_FILE, check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            record_type TEXT NOT NULL,
            record_key TEXT NOT NULL,
            payload TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (record_type, record_key)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runbooks (
            pr_id TEXT PRIMARY KEY,
            title TEXT,
            trust_status TEXT,
            risk TEXT,
            confidence REAL,
            payload TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS validation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_case TEXT,
            baseline_minutes REAL,
            assistant_minutes REAL,
            time_saved REAL,
            reduction_percent REAL,
            result TEXT,
            observation TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def _db_record_type(path):
    name = Path(path).name
    return {
        "audit_log.csv": "audit",
        "trusted_runbooks.csv": "trusted",
        "rollback_log.csv": "rollback",
        "experiment_results.csv": "validation"
    }.get(name, "general")


def _db_read(path):
    """Read persistent records from SQLite."""
    record_type = _db_record_type(path)
    try:
        conn = _db_connect()
        rows = conn.execute(
            "SELECT record_key, payload FROM records WHERE record_type=? ORDER BY record_key",
            (record_type,)
        ).fetchall()
        conn.close()
        return [json.loads(payload) for _, payload in rows]
    except Exception as e:
        st.session_state.persistence_warning = str(e)
        return []


def _db_write(path, records):
    """Replace a record collection in SQLite and keep a CSV export for transparency."""
    record_type = _db_record_type(path)
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = _db_connect()
        conn.execute("DELETE FROM records WHERE record_type=?", (record_type,))
        for i, row in enumerate(records):
            key = str(row.get("PR_ID", row.get("Test Case", i))) + "::" + str(i)
            conn.execute(
                "INSERT OR REPLACE INTO records(record_type,record_key,payload,updated_at) VALUES(?,?,?,?)",
                (record_type, key, json.dumps(row, default=str), now)
            )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.session_state.persistence_warning = str(e)
        return False


def _db_save_runbook(runbook):
    try:
        conn = _db_connect()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            """INSERT OR REPLACE INTO runbooks
            (pr_id,title,trust_status,risk,confidence,payload,updated_at)
            VALUES(?,?,?,?,?,?,?)""",
            (
                str(runbook.get("PR_ID", "")),
                str(runbook.get("Title", "")),
                str(runbook.get("Trust Status", "")),
                "High Impact" if runbook.get("High Impact", False) else "Normal Impact",
                float(runbook.get("Confidence", 0)),
                json.dumps(runbook, default=str),
                now
            )
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.session_state.persistence_warning = str(e)
        return False


def _db_load_runbooks():
    try:
        conn = _db_connect()
        rows = conn.execute("SELECT payload FROM runbooks ORDER BY updated_at").fetchall()
        conn.close()
        return [json.loads(row[0]) for row in rows]
    except Exception as e:
        st.session_state.persistence_warning = str(e)
        return []


def _db_save_validation(experiment):
    try:
        conn = _db_connect()
        conn.execute(
            """INSERT INTO validation_results
            (test_case,baseline_minutes,assistant_minutes,time_saved,reduction_percent,result,observation,created_at)
            VALUES(?,?,?,?,?,?,?,?)""",
            (
                experiment.get("Test Case", ""),
                float(experiment.get("Baseline Minutes", 0)),
                float(experiment.get("Assistant Minutes", 0)),
                float(experiment.get("Time Saved", 0)),
                float(experiment.get("Reduction %", 0)),
                experiment.get("Result", ""),
                experiment.get("Observation", ""),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.session_state.persistence_warning = str(e)
        return False


def _read_records(path):
    """Read durable SQLite records first, with CSV fallback for migration."""
    db_records = _db_read(path)
    if db_records:
        return db_records
    try:
        if not path.exists():
            return []
        df = pd.read_csv(path).fillna("")
        records = df.to_dict("records")
        if records:
            _db_write(path, records)
        return records
    except Exception as e:
        st.session_state.persistence_warning = str(e)
        return []


def _write_records(path, records):
    """Persist records durably in SQLite and also export CSV for inspection."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        db_ok = _db_write(path, records)
        pd.DataFrame(records).to_csv(path, index=False)
        return db_ok
    except Exception as e:
        st.session_state.persistence_warning = str(e)
        return False


def _load_persistent_state():
    if st.session_state.persistence_loaded:
        return

    # Runbooks are indexed durably in SQLite.
    persisted_runbooks = _db_load_runbooks()
    if persisted_runbooks:
        st.session_state.runbooks = persisted_runbooks

    # Audit
    audit_records = _read_records(AUDIT_FILE)
    if audit_records:
        st.session_state.audit_log = audit_records

    # Rollback
    rollback_records = _read_records(ROLLBACK_FILE)
    if rollback_records:
        st.session_state.rollback_log = rollback_records

    # Validation experiments
    experiment_records = _read_records(EXPERIMENT_FILE)
    if experiment_records:
        st.session_state.experiment_results = experiment_records

    # Trusted runbooks
    trusted_records = _read_records(TRUST_FILE)
    for row in trusted_records:
        pr_id = str(row.get("PR_ID", "")).strip()
        if not pr_id:
            continue
        st.session_state.trusted_metadata[pr_id] = row
        if pr_id not in st.session_state.approved_runbooks:
            st.session_state.approved_runbooks.append(pr_id)
        if str(row.get("Human_Confirmed", "")).lower() in {"yes", "true", "1"}:
            if pr_id not in st.session_state.human_confirmations:
                st.session_state.human_confirmations.append(pr_id)

    st.session_state.persistence_loaded = True


def _persist_trusted_state():
    rows = []
    for pr_id, meta in st.session_state.trusted_metadata.items():
        rows.append({
            "PR_ID": pr_id,
            "Trust_Status": meta.get("Trust_Status", "TRUSTED / VERIFIED"),
            "Human_Confirmed": meta.get("Human_Confirmed", "Not Required"),
            "Human_Reviewer": meta.get("Human_Reviewer", ""),
            "Approval_Reason": meta.get("Approval_Reason", ""),
            "Approved_At": meta.get("Approved_At", ""),
            "High_Impact": meta.get("High_Impact", "False")
        })
    _write_records(TRUST_FILE, rows)


def _sync_runbook_trust(runbook):
    """Always add trust fields so old/new runbooks cannot raise KeyError."""
    pr_id = str(runbook.get("PR_ID", ""))
    meta = st.session_state.trusted_metadata.get(pr_id)

    if meta:
        runbook["Trust Status"] = "TRUSTED / VERIFIED"
        runbook["Human Review Status"] = "Approved"
        runbook["Human Confirmation"] = meta.get("Human_Confirmed", "Not Required")
        runbook["Human Reviewer"] = meta.get("Human_Reviewer", "")
        runbook["Approval Reason"] = meta.get("Approval_Reason", "")
        runbook["Approved At"] = meta.get("Approved_At", "")
    elif runbook.get("Verification Status", "Incomplete") == "Verified":
        runbook["Trust Status"] = "PENDING HUMAN APPROVAL"
        runbook["Human Review Status"] = "Pending"
        runbook["Human Confirmation"] = "Required" if runbook.get("High Impact", False) else "Not Required"
        runbook.setdefault("Human Reviewer", "")
        runbook.setdefault("Approval Reason", "")
        runbook.setdefault("Approved At", "")
    else:
        runbook["Trust Status"] = "NOT ELIGIBLE"
        runbook["Human Review Status"] = "Pending Evidence"
        runbook["Human Confirmation"] = "Required" if runbook.get("High Impact", False) else "Not Required"
        runbook.setdefault("Human Reviewer", "")
        runbook.setdefault("Approval Reason", "")
        runbook.setdefault("Approved At", "")

    runbook.setdefault("Rejection Reason", "")
    runbook.setdefault("Rejected At", "")
    return runbook


def _find_runbook(pr_id):
    for runbook in st.session_state.runbooks:
        if str(runbook.get("PR_ID", "")) == str(pr_id):
            return runbook
    return None


def approve_runbook(runbook, reviewer_name, approval_reason, high_impact_confirmation=False, decision="Approve"):
    """Single approval gate used by the human-review workflow."""
    pr_id = str(runbook.get("PR_ID", ""))
    reviewer_name = str(reviewer_name).strip()
    approval_reason = str(approval_reason).strip()

    if not reviewer_name:
        return False, "Human reviewer name is required."
    if not approval_reason:
        return False, "Approval reason is required."
    if get_diff(pr_id) is None:
        return False, "Approval blocked: code diff evidence is missing."
    if get_incident(pr_id) is None:
        return False, "Approval blocked: incident evidence is missing."
    if str(runbook.get("Reviewer Status", "")).lower() != "approved":
        return False, "Approval blocked: source reviewer approval is required."
    if str(runbook.get("Verification Status", "")) != "Verified":
        return False, "Approval blocked: evidence verification is incomplete."
    if runbook.get("High Impact", False) and not high_impact_confirmation:
        return False, "Explicit human confirmation is required for this high-impact runbook."

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    confirmation_text = "Yes" if runbook.get("High Impact", False) else "Not Required"

    runbook["Trust Status"] = "TRUSTED / VERIFIED"
    runbook["Human Review Status"] = "Approved" if decision == "Approve" else "Overridden"
    runbook["Human Confirmation"] = confirmation_text
    runbook["Human Reviewer"] = reviewer_name
    runbook["Approval Reason"] = approval_reason
    runbook["Approved At"] = now
    runbook["Rejection Reason"] = ""
    runbook["Rejected At"] = ""

    if pr_id not in st.session_state.approved_runbooks:
        st.session_state.approved_runbooks.append(pr_id)

    if runbook.get("High Impact", False) and pr_id not in st.session_state.human_confirmations:
        st.session_state.human_confirmations.append(pr_id)

    st.session_state.trusted_metadata[pr_id] = {
        "Trust_Status": "TRUSTED / VERIFIED",
        "Human_Confirmed": confirmation_text,
        "Human_Reviewer": reviewer_name,
        "Approval_Reason": approval_reason,
        "Approved_At": now,
        "High_Impact": str(runbook.get("High Impact", False))
    }
    _persist_trusted_state()
    _db_save_runbook(runbook)

    add_audit(
        "Runbook Approved" if decision == "Approve" else "Runbook Override",
        f"{pr_id} trusted by {reviewer_name}.",
        pr_id=pr_id,
        actor=reviewer_name,
        decision=decision,
        risk="High Impact" if runbook.get("High Impact", False) else "Normal Impact",
        reason=approval_reason,
        confirmation=confirmation_text
    )
    return True, "Runbook is now TRUSTED / VERIFIED."


def reject_runbook(runbook, reviewer_name, rejection_reason):
    pr_id = str(runbook.get("PR_ID", ""))
    reviewer_name = str(reviewer_name).strip()
    rejection_reason = str(rejection_reason).strip()
    if not reviewer_name:
        return False, "Human reviewer name is required."
    if not rejection_reason:
        return False, "Rejection reason is required."

    st.session_state.approved_runbooks = [
        x for x in st.session_state.approved_runbooks
        if str(x) != pr_id
    ]
    st.session_state.trusted_metadata.pop(pr_id, None)
    st.session_state.human_confirmations = [
        x for x in st.session_state.human_confirmations
        if str(x) != pr_id
    ]
    _persist_trusted_state()
    _db_save_runbook(runbook)

    runbook["Trust Status"] = "REJECTED"
    runbook["Human Review Status"] = "Rejected"
    runbook["Human Reviewer"] = reviewer_name
    runbook["Rejection Reason"] = rejection_reason
    runbook["Rejected At"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    add_audit(
        "Runbook Rejected",
        f"{pr_id} rejected by {reviewer_name}.",
        pr_id=pr_id,
        actor=reviewer_name,
        decision="Reject",
        risk="High Impact" if runbook.get("High Impact", False) else "Normal Impact",
        reason=rejection_reason,
        confirmation=str(runbook.get("Human Confirmation", "Not Required"))
    )
    return True, "Runbook rejected and reason recorded."


def revoke_trust(runbook, reviewer_name, reason):
    pr_id = str(runbook.get("PR_ID", ""))
    reviewer_name = str(reviewer_name).strip()
    reason = str(reason).strip()
    if not reviewer_name:
        return False, "Reviewer name is required."
    if not reason:
        return False, "Revocation reason is required."

    st.session_state.trusted_metadata.pop(pr_id, None)
    st.session_state.approved_runbooks = [x for x in st.session_state.approved_runbooks if str(x) != pr_id]
    st.session_state.human_confirmations = [x for x in st.session_state.human_confirmations if str(x) != pr_id]
    _persist_trusted_state()
    _db_save_runbook(runbook)

    runbook["Trust Status"] = "REVOKED"
    runbook["Human Review Status"] = "Trust Revoked"
    add_audit(
        "Trust Revoked",
        f"Trusted status revoked for {pr_id} by {reviewer_name}.",
        pr_id=pr_id,
        actor=reviewer_name,
        decision="Revoke Trust",
        risk="High Impact" if runbook.get("High Impact", False) else "Normal Impact",
        reason=reason,
        confirmation=str(runbook.get("Human Confirmation", "Not Required"))
    )
    return True, "Trust revoked."


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def add_audit(
    action,
    details,
    pr_id="",
    actor="System",
    decision="",
    risk="",
    reason="",
    confirmation=""
):

    st.session_state.audit_log.append(
        {
            "Timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "Actor":
                actor,

            "Action":
                action,

            "PR_ID":
                pr_id,

            "Decision":
                decision,

            "Risk":
                risk,

            "Confirmation":
                confirmation,

            "Reason":
                reason,

            "Details":
                details
        }
    )

    _write_records(
        AUDIT_FILE,
        st.session_state.audit_log
    )


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


_load_persistent_state()


# ============================================================
# RUNBOOK GENERATOR
# ============================================================

# ============================================================
# STRUCTURED EXTRACTION / LIGHTWEIGHT NLP
# ============================================================

def _sentences(text):
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    if not text:
        return []
    return [x.strip(" .") for x in re.split(r"(?<=[.!?])\s+|[;|]", text) if x.strip()]


def extract_root_cause(problem, discussion, resolution):
    """Extract root-cause evidence using transparent phrase/sentence rules."""
    source = f"{problem}. {discussion}. {resolution}"
    cause_terms = ("because", "caused by", "root cause", "due to", "incorrect", "missing", "expired", "timeout", "misconfigured", "configuration", "permission")
    candidates = [s for s in _sentences(source) if any(t in s.lower() for t in cause_terms)]
    if candidates:
        return candidates[0]
    discussion_sentences = _sentences(discussion)
    if discussion_sentences:
        return discussion_sentences[0]
    return "Root cause could not be confidently extracted from the available evidence."


def extract_action_steps(resolution, new_code):
    """Turn resolution/change evidence into short reusable action steps."""
    source = f"{resolution}. {new_code}"
    sentences = _sentences(source)
    steps = []
    action_words = ("update", "change", "replace", "add", "remove", "set", "configure", "restart", "deploy", "enable", "disable", "modify", "fix")
    for sentence in sentences:
        if any(word in sentence.lower() for word in action_words):
            steps.append(sentence)
    if not steps and resolution:
        steps.append(str(resolution).strip())
    return steps[:5]


def extract_verification_steps(resolution, discussion):
    source = f"{resolution}. {discussion}"
    verification_words = ("verify", "test", "confirm", "validated", "working", "resolved", "monitor", "check")
    found = [s for s in _sentences(source) if any(w in s.lower() for w in verification_words)]
    return found[:5]


def build_structured_evidence(problem, discussion, resolution, new_code):
    root = extract_root_cause(problem, discussion, resolution)
    actions = extract_action_steps(resolution, new_code)
    verification_steps = extract_verification_steps(resolution, discussion)
    return {
        "Root Cause Signal": root,
        "Action Steps": actions,
        "Verification Steps": verification_steps,
        "Extraction Method": "Transparent phrase/sentence rules",
    }


def generate_runbook(pr_id):

    pr = get_pr(pr_id)
    incident = get_incident(pr_id)
    diff = get_diff(pr_id)
    review = get_review(pr_id)

    if pr is None:
        return None

    # --------------------------------------------------------
    # Explainable Confidence
    # --------------------------------------------------------
    # Each confidence point comes from a visible evidence rule.
    # PR evidence is required as the base completed-fix source.
    pr_evidence_score = 40

    incident_evidence_score = (
        15 if incident is not None else 0
    )

    diff_evidence_score = (
        15 if diff is not None else 0
    )

    reviewer_evidence_score = 0

    if review is not None:

        if str(
            review["Decision"]
        ).lower() == "approved":

            reviewer_evidence_score = 30

    confidence = min(
        pr_evidence_score
        + incident_evidence_score
        + diff_evidence_score
        + reviewer_evidence_score,
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
    # Structured extraction / lightweight NLP
    # --------------------------------------------------------
    structured_evidence = build_structured_evidence(
        problem,
        root_cause if incident is not None else "",
        str(pr["Resolution"]),
        new_code if diff is not None else ""
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
            structured_evidence["Root Cause Signal"],

        "Structured Evidence":
            structured_evidence,

        "Action Steps":
            structured_evidence["Action Steps"],

        "Verification Steps":
            structured_evidence["Verification Steps"],

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

        "Confidence Rules": {
            "Pull Request": pr_evidence_score,
            "Incident Discussion": incident_evidence_score,
            "Code Diff": diff_evidence_score,
            "Reviewer Approved": reviewer_evidence_score,
        },

        "High Impact":
            high_impact,

        # Trust/verification fields are ALWAYS present. This prevents
        # KeyError when older runbooks are loaded or generated.
        "Trust Status":
            "PENDING HUMAN APPROVAL" if verification_status == "Verified" else "NOT ELIGIBLE",

        "Human Review Status":
            "Pending",

        "Human Confirmation":
            "Required" if high_impact else "Not Required",

        "Human Reviewer":
            "",

        "Approval Reason":
            "",

        "Approved At":
            "",

        "Rejection Reason":
            "",

        "Rejected At":
            "",

        "Created At":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }

    return _sync_runbook_trust(runbook)


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

    st.success(f"🗄️ Persistent storage active: SQLite database at `{SQLITE_FILE.name}`")

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

            existing = _find_runbook(pr_id)

            if existing is None:
                st.session_state.runbooks.append(runbook)
                _db_save_runbook(runbook)
                add_audit(
                    "Runbook Generated",
                    f"Runbook generated for {pr_id}",
                    pr_id=pr_id
                )
            else:
                existing.clear()
                existing.update(runbook)
                _db_save_runbook(existing)
                add_audit(
                    "Runbook Regenerated",
                    f"Runbook regenerated for {pr_id}",
                    pr_id=pr_id
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

            st.write("### 🧠 Structured Extraction")
            st.write("**Root-cause signal:**", runbook.get("Structured Evidence", {}).get("Root Cause Signal", "Not extracted"))
            action_steps = runbook.get("Action Steps", [])
            if action_steps:
                st.write("**Reusable action steps:**")
                for step in action_steps:
                    st.write(f"• {step}")

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
                "### Trust Status"
            )

            trust_status = runbook.get(
                "Trust Status",
                "PENDING HUMAN APPROVAL"
            )

            if trust_status == "TRUSTED / VERIFIED":
                st.success(trust_status)
            elif trust_status == "REJECTED":
                st.error(trust_status)
            else:
                st.warning(trust_status)

            st.write(
                "### Human Reviewer"
            )
            st.write(runbook.get("Human Reviewer", "" ) or "Not approved yet")

            st.write(
                "### Confidence"
            )

            st.progress(
                runbook["Confidence"] / 100
            )

            st.write(
                f"{runbook['Confidence']}%"
            )

        st.write("### 🧪 Verification Steps")
        verification_steps = runbook.get("Verification Steps", [])
        if verification_steps:
            for step in verification_steps:
                st.write(f"• {step}")
        else:
            st.info("No explicit verification sentence was extracted; reviewer verification is still required.")

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

        # ============================================================
        # CONFIDENCE RULES EXPLANATION
        # ============================================================

        st.divider()

        st.subheader(
            "📐 Confidence Calculation"
        )

        st.write(
            "The confidence score is calculated from four explicit "
            "evidence rules. The score is capped at 100%."
        )

        confidence_rules = runbook["Confidence Rules"]

        rule_col1, rule_col2 = st.columns(2)

        with rule_col1:

            if confidence_rules["Pull Request"] > 0:
                st.success(
                    f"✓ Pull Request available  +{confidence_rules['Pull Request']}"
                )
            else:
                st.error(
                    "✗ Pull Request evidence missing  +0"
                )

            if confidence_rules["Incident Discussion"] > 0:
                st.success(
                    f"✓ Incident discussion available  +{confidence_rules['Incident Discussion']}"
                )
            else:
                st.warning(
                    "⚠ Incident discussion unavailable  +0"
                )

        with rule_col2:

            if confidence_rules["Code Diff"] > 0:
                st.success(
                    f"✓ Code diff available  +{confidence_rules['Code Diff']}"
                )
            else:
                st.warning(
                    "⚠ Code diff unavailable  +0"
                )

            if confidence_rules["Reviewer Approved"] > 0:
                st.success(
                    f"✓ Reviewer approved  +{confidence_rules['Reviewer Approved']}"
                )
            else:
                st.warning(
                    "⚠ Reviewer approval not confirmed  +0"
                )

        st.divider()

        st.write(
            "### 🧮 Score Calculation"
        )

        score_parts = [
            confidence_rules["Pull Request"],
            confidence_rules["Incident Discussion"],
            confidence_rules["Code Diff"],
            confidence_rules["Reviewer Approved"],
        ]

        st.code(
            " + ".join(str(x) for x in score_parts)
            + f" = {runbook['Confidence']}%"
        )

        st.metric(
            "Final Confidence",
            f"{runbook['Confidence']}%"
        )

        st.caption(
            "Rule weights: PR = 40, Incident = 15, "
            "Code Diff = 15, Reviewer Approval = 30."
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

    st.title("✅ Human Review & Trust Gate")

    st.write(
        "Every reusable runbook must pass evidence checks and a human review. "
        "High-impact runbooks additionally require explicit human confirmation."
    )

    if not st.session_state.runbooks:
        st.info("Generate a runbook first.")
    else:
        for index, runbook in enumerate(st.session_state.runbooks):
            _sync_runbook_trust(runbook)
            pr_id = str(runbook.get("PR_ID", ""))
            trust_status = runbook.get("Trust Status", "PENDING HUMAN APPROVAL")

            st.divider()
            st.subheader(f"{pr_id} - {runbook.get('Title', '')}")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Confidence", f"{runbook.get('Confidence', 0)}%")
            with c2:
                st.metric("Verification", runbook.get("Verification Status", "Unknown"))
            with c3:
                if trust_status == "TRUSTED / VERIFIED":
                    st.success("TRUSTED / VERIFIED")
                elif trust_status == "REJECTED":
                    st.error("REJECTED")
                else:
                    st.warning(trust_status)

            # Required evidence gates
            incident_ok = get_incident(pr_id) is not None
            diff_ok = get_diff(pr_id) is not None
            reviewer_ok = str(runbook.get("Reviewer Status", "")).lower() == "approved"
            verification_ok = runbook.get("Verification Status") == "Verified"

            st.write("### Evidence Gate")
            st.write(f"{'✅' if incident_ok else '❌'} Incident evidence")
            st.write(f"{'✅' if diff_ok else '❌'} Code diff evidence")
            st.write(f"{'✅' if reviewer_ok else '❌'} Source reviewer approval")
            st.write(f"{'✅' if verification_ok else '❌'} Evidence verification")

            if trust_status == "TRUSTED / VERIFIED":
                st.success(
                    f"Trusted by {runbook.get('Human Reviewer', 'human reviewer')} "
                    f"at {runbook.get('Approved At', '')}."
                )
                st.info(
                    f"Approval reason: {runbook.get('Approval Reason', '')}"
                )

                revoke_reviewer = st.text_input(
                    "Reviewer name to revoke trust",
                    key=f"revoke_reviewer_{index}",
                    placeholder="Example: Reviewer001"
                )
                revoke_reason = st.text_area(
                    "Reason for revoking trust",
                    key=f"revoke_reason_{index}",
                    placeholder="Example: New evidence invalidated the runbook."
                )
                if st.button("↩️ Revoke Trust", key=f"revoke_{index}"):
                    ok, message = revoke_trust(runbook, revoke_reviewer, revoke_reason)
                    if ok:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                continue

            if not diff_ok:
                st.error("❌ Approval blocked: Code diff is missing.")
                continue
            if not incident_ok:
                st.error("❌ Approval blocked: Incident evidence is missing.")
                continue
            if not reviewer_ok:
                st.warning("⏳ Approval blocked: Source reviewer approval is required.")
                continue
            if not verification_ok:
                st.warning("⏳ Approval blocked: Evidence verification is incomplete.")
                continue

            reviewer_name = st.text_input(
                "Human reviewer name",
                value=runbook.get("Human Reviewer", ""),
                key=f"human_reviewer_{index}",
                placeholder="Example: Reviewer001"
            )

            decision = st.radio(
                "Human Decision",
                ["Approve", "Reject", "Override"],
                key=f"decision_{index}",
                horizontal=True
            )

            confirmation = True
            if runbook.get("High Impact", False):
                st.warning(
                    "⚠️ HIGH-IMPACT ACTION: explicit human confirmation is mandatory."
                )
                confirmation = st.checkbox(
                    "I confirm that this high-impact runbook has been manually reviewed and I understand the rollback path.",
                    key=f"confirm_{index}",
                    value=(str(runbook.get("Human Confirmation", "")) == "Yes")
                )

            approval_reason = st.text_area(
                "Approval / override reason" if decision != "Reject" else "Rejection reason",
                value=(runbook.get("Approval Reason", "") if decision != "Reject" else runbook.get("Rejection Reason", "")),
                key=f"decision_reason_{index}",
                placeholder="Explain the human decision and evidence checked."
            )

            if st.button(
                "💾 Submit Human Decision",
                key=f"submit_decision_{index}",
                type="primary"
            ):
                if decision == "Reject":
                    ok, message = reject_runbook(runbook, reviewer_name, approval_reason)
                else:
                    ok, message = approve_runbook(
                        runbook,
                        reviewer_name,
                        approval_reason,
                        high_impact_confirmation=confirmation,
                        decision=decision
                    )

                if ok:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    if st.session_state.approved_runbooks:
        st.divider()
        st.subheader("✅ Trusted Runbooks")
        trusted_rows = []
        for pr_id in st.session_state.approved_runbooks:
            meta = st.session_state.trusted_metadata.get(str(pr_id), {})
            trusted_rows.append({
                "PR_ID": pr_id,
                "Trust Status": meta.get("Trust_Status", "TRUSTED / VERIFIED"),
                "Human Reviewer": meta.get("Human_Reviewer", ""),
                "Approval Reason": meta.get("Approval_Reason", ""),
                "Approved At": meta.get("Approved_At", "")
            })
        st.dataframe(pd.DataFrame(trusted_rows), use_container_width=True, hide_index=True)


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
        "🔄 Change Review & Rollback Manager"
    )

    st.warning(
        """
        Prototype simulation only.

        This feature does NOT modify production code.
        It records the change-review decision and the rollback path.
        High-impact changes require explicit human confirmation.
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
        # CHANGE REVIEW
        # --------------------------------------------------------

        st.divider()

        st.subheader(
            "🔍 Change Review"
        )

        if high_impact:

            st.error(
                "🚨 HIGH-IMPACT CHANGE"
            )

            st.write(
                "Human review and explicit confirmation are required "
                "before this change can be accepted as a trusted maintenance change."
            )

        else:

            st.success(
                "✅ NORMAL-IMPACT CHANGE"
            )

            st.write(
                "Standard human change review is required."
            )

        review_actor = st.text_input(
            "Reviewer / Change Owner",
            placeholder="Example: Reviewer001"
        )

        review_decision = st.radio(
            "Change Review Decision",
            [
                "Approve Change",
                "Reject Change"
            ],
            horizontal=True
        )

        if high_impact:

            change_confirmation = st.checkbox(
                "I confirm that I reviewed the high-impact change, "
                "understand the risk, and have checked the rollback path."
            )

        else:

            change_confirmation = True

        change_reason = st.text_area(
            "Change Review Reason",
            placeholder=(
                "Explain why this change is approved or rejected..."
            )
        )

        if st.button(
            "📋 Record Change Review",
            type="primary"
        ):

            if not review_actor.strip():

                st.error(
                    "Reviewer / Change Owner is required."
                )

            elif high_impact and not change_confirmation:

                st.error(
                    "Explicit human confirmation is required for high-impact changes."
                )

            elif not change_reason.strip():

                st.error(
                    "Change review reason is required."
                )

            else:

                review_record = {

                    "PR_ID":
                        pr_id,

                    "Reviewer":
                        review_actor,

                    "Decision":
                        review_decision,

                    "Risk":
                        "High Impact" if high_impact else "Normal Impact",

                    "Confirmation":
                        bool(change_confirmation),

                    "Reason":
                        change_reason,

                    "Timestamp":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                }

                st.session_state.change_review_log.append(
                    review_record
                )

                add_audit(
                    "Change Review Recorded",
                    f"{pr_id}: {review_decision}",
                    pr_id=pr_id,
                    actor=review_actor,
                    decision=review_decision,
                    risk=(
                        "High Impact"
                        if high_impact
                        else "Normal Impact"
                    ),
                    reason=change_reason,
                    confirmation=str(change_confirmation)
                )

                if review_decision == "Approve Change":

                    st.success(
                        "✅ Change review approved and recorded."
                    )

                else:

                    st.warning(
                        "⚠️ Change review rejected and recorded."
                    )

        # --------------------------------------------------------
        # CHANGE REVIEW HISTORY
        # --------------------------------------------------------

        if st.session_state.change_review_log:

            st.write(
                "### 📋 Change Review History"
            )

            st.dataframe(
                pd.DataFrame(
                    st.session_state.change_review_log
                ),
                use_container_width=True
            )

        # --------------------------------------------------------
        # ROLLBACK PATH
        # --------------------------------------------------------

        st.divider()

        st.subheader(
            "🔄 Rollback Path"
        )

        st.write(
            "The rollback path records what would be restored, "
            "why rollback is required, and who confirmed it. "
            "No production code is changed by this prototype."
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

        if high_impact:

            rollback_confirmation = st.checkbox(
                "I confirm that rollback is required and I have reviewed the rollback path."
            )

        else:

            rollback_confirmation = True

        rollback_actor = st.text_input(
            "Rollback Reviewer",
            placeholder="Example: Reviewer001",
            key=f"rollback_actor_{pr_id}"
        )

        reason = st.text_area(
            "Rollback Reason",
            placeholder="Explain why the rollback is required...",
            key=f"rollback_reason_{pr_id}"
        )

        if st.button(
            "🔄 Record Rollback",
            type="secondary"
        ):

            if not rollback_actor.strip():

                st.error(
                    "Rollback reviewer is required."
                )

            elif not rollback_confirmation:

                st.error(
                    "Human confirmation is required for this rollback."
                )

            elif not reason.strip():

                st.error(
                    "Rollback reason is required."
                )

            else:

                record = {

                    "PR_ID":
                        pr_id,

                    "Reviewer":
                        rollback_actor,

                    "Reason":
                        reason,

                    "Risk":
                        "High Impact" if high_impact else "Normal Impact",

                    "Confirmation":
                        bool(rollback_confirmation),

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

                _write_records(
                    ROLLBACK_FILE,
                    st.session_state.rollback_log
                )

                add_audit(
                    "Rollback Recorded",
                    f"{pr_id}: {reason}",
                    pr_id=pr_id,
                    actor=rollback_actor,
                    decision="Rollback",
                    risk=(
                        "High Impact"
                        if high_impact
                        else "Normal Impact"
                    ),
                    reason=reason,
                    confirmation=str(rollback_confirmation)
                )

                st.success(
                    "✅ Rollback path recorded successfully."
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

    st.title("⚠️ Risk Checker")

    st.write(
        "The prototype uses explainable keyword rules to identify potentially high-impact changes."
    )

    st.info(
        "High-impact keywords: authentication • security • password • permission • database • payment • delete • production • credential • access"
    )

    pr_id = st.selectbox("Select Pull Request", pull_requests["PR_ID"].tolist())
    pr = get_pr(pr_id)

    if pr is not None:
        combined_text = f"{pr['Title']} {pr['Description']} {pr['Resolution']}"
        high_impact = is_high_impact(combined_text)
        runbook = _find_runbook(pr_id)

        if high_impact:
            st.error("🚨 HIGH-IMPACT CHANGE")
            st.write("Human confirmation is required before this change can become trusted maintenance knowledge.")
        else:
            st.success("✅ NORMAL-IMPACT CHANGE")

        if runbook is None:
            if st.button("📘 Generate Evidence-Backed Runbook", type="primary"):
                generated = generate_runbook(pr_id)
                if generated:
                    st.session_state.runbooks.append(generated)
                    _db_save_runbook(generated)
                    add_audit("Runbook Generated", f"Runbook generated from Risk Checker for {pr_id}", pr_id=pr_id)
                    st.rerun()
        else:
            _sync_runbook_trust(runbook)
            st.write(f"**Trust Status:** {runbook.get('Trust Status', 'PENDING HUMAN APPROVAL')}")
            st.write(f"**Verification:** {runbook.get('Verification Status', 'Unknown')}")

            if high_impact and runbook.get("Trust Status") != "TRUSTED / VERIFIED":
                confirmation = st.checkbox(
                    "I confirm that I have manually reviewed this high-impact runbook and checked the rollback path.",
                    key=f"risk_confirm_{pr_id}",
                    value=(pr_id in st.session_state.human_confirmations)
                )
                reviewer = st.text_input(
                    "Human reviewer name",
                    key=f"risk_reviewer_{pr_id}",
                    placeholder="Example: Reviewer001"
                )
                reason = st.text_area(
                    "Human confirmation / approval reason",
                    key=f"risk_reason_{pr_id}",
                    placeholder="Explain what evidence you checked."
                )

                if st.button("🔐 Confirm & Approve as Trusted Knowledge", key=f"risk_approve_{pr_id}", type="primary"):
                    ok, message = approve_runbook(
                        runbook,
                        reviewer,
                        reason,
                        high_impact_confirmation=confirmation,
                        decision="Approve"
                    )
                    if ok:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            elif runbook.get("Trust Status") == "TRUSTED / VERIFIED":
                st.success("🟢 This runbook is already TRUSTED / VERIFIED.")
            else:
                st.info("Normal-impact runbooks still require standard human review in Review Runbooks.")


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

        st.caption(f"Durable SQLite store: {SQLITE_FILE}  |  CSV export: {AUDIT_FILE}")

        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download Audit Trail CSV",
            audit_df.to_csv(index=False),
            file_name="maintenance_audit_trail.csv",
            mime="text/csv"
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

    st.title(
        "📊 Validation Dashboard"
    )

    st.write(
        """
        Measure whether the assistant reduces the time required
        for a new engineer to repeat a known maintenance fix.
        """
    )

    st.subheader(
        "➕ Add Experiment Result"
    )

    col1, col2 = st.columns(2)

    with col1:

        test_case = st.text_input(
            "Test Case",
            placeholder="Example: Redis timeout fix"
        )

        baseline_time = st.number_input(
            "Baseline Time (minutes)",
            min_value=1.0,
            value=60.0
        )

    with col2:

        assistant_time = st.number_input(
            "With Assistant (minutes)",
            min_value=1.0,
            value=30.0
        )

        tester = st.text_input(
            "Tester / Engineer ID (anonymised)",
            placeholder="Example: Engineer-01"
        )

        correctness = st.selectbox(
            "Recommendation correctness",
            ["Correct", "Partially Correct", "Incorrect"]
        )

        result = st.selectbox(
            "Result",
            [
                "Success",
                "Partial Success",
                "Failure"
            ]
        )

    observation = st.text_area(
        "Observation / Error Analysis",
        placeholder="Describe what happened during the test..."
    )

    if st.button(
        "➕ Add Result",
        type="primary"
    ):

        if not test_case.strip():

            st.error(
                "Please enter a test case."
            )

        else:

            # Do not block regressions. Negative reduction is valuable
            # validation evidence and belongs in error analysis.
            time_saved = (
                baseline_time
                - assistant_time
            )

            reduction = (
                time_saved
                / baseline_time
            ) * 100

            experiment = {

                "Test Case":
                    test_case,

                "Baseline Minutes":
                    baseline_time,

                "Assistant Minutes":
                    assistant_time,

                "Time Saved":
                    time_saved,

                "Reduction %":
                    reduction,

                "Tester":
                    tester.strip(),

                "Correctness":
                    correctness,

                "Result":
                    result,

                "Observation":
                    observation
            }

            st.session_state.experiment_results.append(
                experiment
            )

            _write_records(
                EXPERIMENT_FILE,
                st.session_state.experiment_results
            )
            _db_save_validation(experiment)

            add_audit(
                "Validation Result Added",
                test_case
            )

            st.success(
                "Validation result added successfully."
            )

    # ========================================================
    # DISPLAY VALIDATION RESULTS
    # ========================================================

    if st.session_state.experiment_results:

        results_df = pd.DataFrame(
            st.session_state.experiment_results
        )

        st.divider()

        st.subheader(
            "📈 Experiment Metrics"
        )

        avg_baseline = results_df[
            "Baseline Minutes"
        ].mean()

        avg_assistant = results_df[
            "Assistant Minutes"
        ].mean()

        avg_saved = results_df[
            "Time Saved"
        ].mean()

        avg_reduction = results_df[
            "Reduction %"
        ].mean()

        median_reduction = results_df["Reduction %"].median()
        reduction_std = results_df["Reduction %"].std(ddof=1) if len(results_df) > 1 else 0.0
        regression_count = int((results_df["Reduction %"] < 0).sum())
        correctness_rate = (results_df["Correctness"] == "Correct").mean() * 100 if "Correctness" in results_df.columns else 0.0
        success_rate = (
            results_df["Result"]
            == "Success"
        ).mean() * 100

        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

        with col1:

            st.metric(
                "Avg Baseline",
                f"{avg_baseline:.1f} min"
            )

        with col2:

            st.metric(
                "Avg Assistant",
                f"{avg_assistant:.1f} min"
            )

        with col3:

            st.metric(
                "Avg Time Saved",
                f"{avg_saved:.1f} min"
            )

        with col4:

            st.metric(
                "Avg Reduction",
                f"{avg_reduction:.1f}%"
            )

        with col5:

            st.metric(
                "Success Rate",
                f"{success_rate:.1f}%"
            )
        with col6:
            st.metric("Median Reduction", f"{median_reduction:.1f}%")
        with col7:
            st.metric("Correctness", f"{correctness_rate:.1f}%")
        with col8:
            st.metric("Regressions", str(regression_count))

        st.caption(f"Reduction standard deviation: {reduction_std:.1f} percentage points. Negative reduction means the assistant was slower and is retained for error analysis.")

        # ----------------------------------------------------
        # TARGET
        # ----------------------------------------------------

        target = 30

        st.subheader(
            "🎯 Target"
        )

        if avg_reduction >= target:

            st.success(
                f"""
                Target achieved!

                Target: {target}% reduction

                Measured: {avg_reduction:.1f}% reduction
                """
            )

        else:

            st.warning(
                f"""
                Target not yet achieved.

                Target: {target}% reduction

                Measured: {avg_reduction:.1f}% reduction
                """
            )

        # ----------------------------------------------------
        # STATISTICAL / ERROR ANALYSIS
        # ----------------------------------------------------
        st.subheader("📐 Evaluation Analysis")
        st.write(f"**Cases evaluated:** {len(results_df)}")
        st.write(f"**Median reduction:** {median_reduction:.1f}%")
        st.write(f"**Variation (sample SD):** {reduction_std:.1f} percentage points")
        st.write(f"**Correct recommendations:** {int((results_df.get('Correctness', pd.Series(dtype=str)) == 'Correct').sum()) if 'Correctness' in results_df.columns else 'Not recorded'}")
        st.write(f"**Regressions (assistant slower):** {regression_count}")
        if regression_count:
            st.warning("Regression cases are retained rather than hidden; review their observations before claiming improvement.")
        else:
            st.success("No regression cases recorded in the current sample.")

        # ----------------------------------------------------
        # RESULTS TABLE
        # ----------------------------------------------------

        st.subheader(
            "📋 Experiment Results"
        )

        st.dataframe(
            results_df,
            use_container_width=True
        )

        # ----------------------------------------------------
        # SIMPLE VISUAL COMPARISON
        # ----------------------------------------------------

        st.subheader(
            "⏱️ Time Comparison"
        )

        for _, row in results_df.iterrows():

            st.write(
                f"**{row['Test Case']}**"
            )

            baseline = float(
                row["Baseline Minutes"]
            )

            assistant = float(
                row["Assistant Minutes"]
            )

            percentage = int(
                min(
                    (assistant / baseline) * 100,
                    100
                )
            )

            st.write(
                f"Baseline: {baseline:.1f} minutes"
            )

            st.progress(
                100
            )

            st.write(
                f"Assistant: {assistant:.1f} minutes"
            )

            st.progress(
                percentage
            )

            st.write(
                f"Time saved: "
                f"{row['Time Saved']:.1f} minutes "
                f"({row['Reduction %']:.1f}%)"
            )

            st.divider()

        # ----------------------------------------------------
        # ERROR ANALYSIS
        # ----------------------------------------------------

        st.subheader(
            "🔍 Error Analysis"
        )

        failures = results_df[
            results_df["Result"] != "Success"
        ]

        if failures.empty:

            st.success(
                "No failed or partial validation cases recorded."
            )

        else:

            st.warning(
                f"{len(failures)} validation case(s) "
                "need further analysis."
            )

            st.dataframe(
                failures[
                    [
                        "Test Case",
                        "Result",
                        "Observation"
                    ]
                ],
                use_container_width=True
            )

    else:

        st.info(
            "Add experiment results to display validation metrics."
        )


# ============================================================
# END
# ============================================================
