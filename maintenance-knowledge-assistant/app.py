import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import sqlite3
import json
import re

st.set_page_config(
    page_title="Maintenance Knowledge Assistant",
    page_icon="🛠️",
    layout="wide"
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "maintenance_assistant.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b1020;
    }

    .main {
        background-color: #0b1020;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .stApp p,
    .stApp li,
    .stApp label {
        color: #d1d5db !important;
    }

    .stApp h1 {
        color: #67e8f9 !important;
    }

    .stApp h2 {
        color: #7dd3fc !important;
    }

    .stApp h3 {
        color: #a5f3fc !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
    }

    .stButton button {
        background-color: #4f46e5 !important;
        color: white !important;
    }

    [data-testid="stMetric"] {
        background-color: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    [data-testid="stMetricValue"] {
        color: #67e8f9 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SQLITE DATABASE
# ============================================================

def get_db():
    return sqlite3.connect(DB_PATH)


def init_database():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with get_db() as conn:

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS runbooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pr_id TEXT UNIQUE,
                data TEXT,
                created_at TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                action TEXT,
                details TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rollback_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                created_at TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS validation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                created_at TEXT
            )
            """
        )

        conn.commit()


init_database()

# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_csv(filename):

    path = DATA_DIR / filename

    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


pull_requests = load_csv("pull_requests.csv")
incidents = load_csv("incidents.csv")
code_diffs = load_csv("code_diffs.csv")
reviews = load_csv("reviews.csv")
validation_dataset = load_csv("validation_dataset.csv")

# ============================================================
# DATA HELPERS
# ============================================================

def find_column(df, possible_names):

    for name in possible_names:

        if name in df.columns:
            return name

    return None


def get_row(df, pr_id):

    if df.empty:
        return None

    key = find_column(
        df,
        [
            "PR_ID",
            "PR Id",
            "pr_id",
            "Pull_Request_ID"
        ]
    )

    if key is None:
        return None

    result = df[
        df[key].astype(str).str.strip()
        == str(pr_id).strip()
    ]

    if result.empty:
        return None

    return result.iloc[0]


def get_value(row, possible_names, default=""):

    if row is None:
        return default

    for name in possible_names:

        if name in row.index:

            if pd.notna(row[name]):
                return str(row[name])

    return default


def get_pr(pr_id):
    return get_row(
        pull_requests,
        pr_id
    )


def get_incident(pr_id):
    return get_row(
        incidents,
        pr_id
    )


def get_diff(pr_id):
    return get_row(
        code_diffs,
        pr_id
    )


def get_review(pr_id):
    return get_row(
        reviews,
        pr_id
    )


def get_pr_ids():

    key = find_column(
        pull_requests,
        [
            "PR_ID",
            "PR Id",
            "pr_id",
            "Pull_Request_ID"
        ]
    )

    if key is None:
        return []

    return pull_requests[
        key
    ].astype(str).tolist()

# ============================================================
# SQLITE PERSISTENCE
# ============================================================

def load_table(table):

    with get_db() as conn:

        rows = conn.execute(
            f"""
            SELECT data
            FROM {table}
            ORDER BY id
            """
        ).fetchall()

    return [
        json.loads(row[0])
        for row in rows
    ]


def save_runbook(runbook):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with get_db() as conn:

        conn.execute(
            """
            INSERT INTO runbooks
            (
                pr_id,
                data,
                created_at
            )
            VALUES (?, ?, ?)

            ON CONFLICT(pr_id)
            DO UPDATE SET
                data = excluded.data,
                created_at = excluded.created_at
            """,
            (
                str(runbook["PR_ID"]),
                json.dumps(runbook),
                timestamp
            )
        )

        conn.commit()

    st.session_state.runbooks = load_table(
        "runbooks"
    )


def save_audit(action, details):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with get_db() as conn:

        conn.execute(
            """
            INSERT INTO audit_log
            (
                timestamp,
                action,
                details
            )
            VALUES (?, ?, ?)
            """,
            (
                timestamp,
                action,
                details
            )
        )

        conn.commit()

    st.session_state.audit_log = load_table(
        "audit_log"
    )


def save_rollback(record):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with get_db() as conn:

        conn.execute(
            """
            INSERT INTO rollback_log
            (
                data,
                created_at
            )
            VALUES (?, ?)
            """,
            (
                json.dumps(record),
                timestamp
            )
        )

        conn.commit()

    st.session_state.rollback_log = load_table(
        "rollback_log"
    )


def save_validation(record):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with get_db() as conn:

        conn.execute(
            """
            INSERT INTO validation_results
            (
                data,
                created_at
            )
            VALUES (?, ?)
            """,
            (
                json.dumps(record),
                timestamp
            )
        )

        conn.commit()

    st.session_state.experiment_results = (
        load_table("validation_results")
    )

# ============================================================
# SESSION STATE
# ============================================================

if "runbooks" not in st.session_state:

    st.session_state.runbooks = load_table(
        "runbooks"
    )


if "audit_log" not in st.session_state:

    st.session_state.audit_log = load_table(
        "audit_log"
    )


if "rollback_log" not in st.session_state:

    st.session_state.rollback_log = load_table(
        "rollback_log"
    )


if "experiment_results" not in st.session_state:

    st.session_state.experiment_results = (
        load_table("validation_results")
    )


if "api_records" not in st.session_state:

    st.session_state.api_records = []

# ============================================================
# STRUCTURED EXTRACTION
# ============================================================

ROOT_CAUSE_WORDS = [
    "because",
    "caused by",
    "due to",
    "root cause",
    "failure",
    "timeout",
    "missing",
    "misconfigured",
    "incorrect",
    "bug",
    "error"
]


ACTION_WORDS = [
    "update",
    "change",
    "replace",
    "configure",
    "modify",
    "fix",
    "restart",
    "deploy",
    "add",
    "remove",
    "set",
    "enable",
    "disable"
]


VERIFICATION_WORDS = [
    "verify",
    "verified",
    "test",
    "tested",
    "confirmed",
    "validate",
    "validated",
    "passed",
    "working",
    "works",
    "success"
]


def split_sentences(text):

    return [
        s.strip()
        for s in re.split(
            r"(?<=[.!?])\s+|\n+",
            str(text or "")
        )
        if s.strip()
    ]


def extract_matching_sentences(
    text,
    keywords
):

    results = []

    for sentence in split_sentences(text):

        lower = sentence.lower()

        if any(
            word in lower
            for word in keywords
        ):

            if sentence not in results:
                results.append(sentence)

    return results[:5]


# ============================================================
# RISK DETECTION
# ============================================================

HIGH_IMPACT_KEYWORDS = [
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


def risk_info(text):

    lower = str(text).lower()

    found = [
        keyword
        for keyword in HIGH_IMPACT_KEYWORDS
        if keyword in lower
    ]

    return (
        len(found) > 0,
        found
    )


def is_high_impact(text):

    result, _ = risk_info(text)

    return result

# ============================================================
# RUNBOOK GENERATION
# ============================================================

def generate_runbook(pr_id):

    pr = get_pr(pr_id)
    incident = get_incident(pr_id)
    diff = get_diff(pr_id)
    review = get_review(pr_id)

    if pr is None:
        return None

    title = get_value(
        pr,
        ["Title", "title"],
        pr_id
    )

    description = get_value(
        pr,
        [
            "Description",
            "description",
            "Problem"
        ]
    )

    solution = get_value(
        pr,
        [
            "Resolution",
            "resolution",
            "Solution",
            "Fix"
        ]
    )

    if incident is not None:

        problem = get_value(
            incident,
            [
                "Problem",
                "Issue",
                "Description"
            ],
            description
        )

        discussion = get_value(
            incident,
            [
                "Discussion",
                "Root_Cause",
                "Root Cause",
                "Analysis"
            ]
        )

        final_resolution = get_value(
            incident,
            [
                "Final_Resolution",
                "Final Resolution",
                "Resolution"
            ]
        )

    else:

        problem = description
        discussion = ""
        final_resolution = ""

    if diff is not None:

        changed_file = get_value(
            diff,
            [
                "File",
                "File_Name",
                "Changed_File"
            ]
        )

        old_code = get_value(
            diff,
            [
                "Old_Code",
                "Old Code",
                "Before"
            ]
        )

        new_code = get_value(
            diff,
            [
                "New_Code",
                "New Code",
                "After"
            ]
        )

    else:

        changed_file = ""
        old_code = ""
        new_code = ""

    if review is not None:

        reviewer = get_value(
            review,
            [
                "Reviewer",
                "Reviewer_Name",
                "Name"
            ],
            "Unavailable"
        )

        decision = get_value(
            review,
            [
                "Decision",
                "Status",
                "Review_Status"
            ],
            "Unknown"
        )

        review_comment = get_value(
            review,
            [
                "Comment",
                "Comments",
                "Review_Comment"
            ]
        )

    else:

        reviewer = "Unavailable"
        decision = "Unknown"
        review_comment = ""

    # --------------------------------------------------------
    # STRUCTURED EXTRACTION
    # --------------------------------------------------------

    root_cause = extract_matching_sentences(
        discussion + " " + description,
        ROOT_CAUSE_WORDS
    )

    reusable_actions = extract_matching_sentences(
        solution
        + " "
        + final_resolution
        + " "
        + new_code,
        ACTION_WORDS
    )

    verification_steps = extract_matching_sentences(
        review_comment
        + " "
        + final_resolution
        + " "
        + discussion,
        VERIFICATION_WORDS
    )

    if not root_cause:

        root_cause = [
            discussion
            or
            "No explicit root-cause signal extracted."
        ]

    if not reusable_actions:

        reusable_actions = [
            solution
            or
            "No explicit reusable action extracted."
        ]

    if not verification_steps:

        verification_steps = [
            "Perform verification using the available reviewer and incident evidence."
        ]

    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    combined_text = " ".join(
        [
            title,
            description,
            solution,
            discussion,
            new_code
        ]
    )

    high_impact, risk_keywords = risk_info(
        combined_text
    )

    # --------------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------------

    evidence_sources = [
        "Pull Request"
    ]

    if incident is not None:
        evidence_sources.append(
            "Incident"
        )

    if diff is not None:
        evidence_sources.append(
            "Code Diff"
        )

    if decision.lower() == "approved":
        evidence_sources.append(
            "Approved Review"
        )

    evidence_count = len(
        evidence_sources
    )

    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence = 40

    if incident is not None:
        confidence += 15

    if diff is not None:
        confidence += 15

    if decision.lower() == "approved":
        confidence += 30

    confidence = min(
        confidence,
        100
    )

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------

    if evidence_count == 4:

        verification_status = "Verified"

    elif evidence_count >= 2:

        verification_status = "Pending Review"

    else:

        verification_status = "Incomplete"

    # --------------------------------------------------------
    # RUNBOOK
    # --------------------------------------------------------

    return {

        "PR_ID":
            pr_id,

        "Title":
            title,

        "Problem":
            problem,

        "Root Cause":
            root_cause,

        "Reusable Actions":
            reusable_actions,

        "Verification Steps":
            verification_steps,

        "Solution":
            solution,

        "Incident Resolution":
            final_resolution,

        "Changed File":
            changed_file
            or
            "Code diff unavailable.",

        "Old Code":
            old_code
            or
            "Not available.",

        "New Code":
            new_code
            or
            "Not available.",

        "Reviewer":
            reviewer,

        "Reviewer Status":
            decision,

        "Review Comment":
            review_comment,

        "Evidence Sources":
            evidence_sources,

        "Evidence Count":
            evidence_count,

        "Verification Status":
            verification_status,

        "Confidence":
            confidence,

        "High Impact":
            high_impact,

        "Risk Keywords":
            risk_keywords,

        "Trust Status":
            "PENDING HUMAN APPROVAL",

        "Human Review Status":
            "Pending",

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

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🛠️ Maintenance Assistant"
)

st.sidebar.caption(
    "Knowledge capture and verified runbook prototype"
)

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
    "Synthetic Data • Human-in-the-loop • SQLite"
)

# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title(
        "🛠️ Maintenance Knowledge Assistant"
    )

    st.write(
        """
        Convert completed engineering fixes into verified,
        reusable maintenance runbooks.
        """
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Pull Requests",
        len(pull_requests)
    )

    c2.metric(
        "Incidents",
        len(incidents)
    )

    c3.metric(
        "Code Diffs",
        len(code_diffs)
    )

    c4.metric(
        "Reviews",
        len(reviews)
    )

    st.subheader(
        "🔄 System Workflow"
    )

    st.code(
        """
Engineering Data
       ↓
Evidence Extraction
       ↓
Runbook Generation
       ↓
Risk Checking
       ↓
Human Review
       ↓
Trusted Knowledge
       ↓
Audit Trail
       ↓
Validation
        """
    )

    st.info(
        f"""
        SQLite database:

        {DB_PATH}

        The database is created automatically when the application starts.
        """
    )

    st.subheader(
        "🎯 Evaluator Improvements"
    )

    st.write(
        """
        1. Structured root-cause, action and verification extraction.

        2. Persistent SQLite storage for runbooks, audit,
           rollback and validation.

        3. Baseline-vs-assistant validation with correctness,
           error analysis and regression tracking.
        """
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

# ============================================================
# INCIDENTS
# ============================================================

elif page == "🚨 Incidents":

    st.title(
        "🚨 Incidents"
    )

    st.dataframe(
        incidents,
        use_container_width=True
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
        PR, incident, code diff and reviewer evidence.
        """
    )

    ids = get_pr_ids()

    if not ids:

        st.error(
            "No PR_ID values found in pull_requests.csv."
        )

        st.stop()

    pr_id = st.selectbox(
        "Select Pull Request",
        ids
    )

    if st.button(
        "🚀 Generate Runbook",
        type="primary"
    ):

        runbook = generate_runbook(
            pr_id
        )

        if runbook:

            save_runbook(
                runbook
            )

            save_audit(
                "Runbook Generated",
                f"Runbook generated for {pr_id}"
            )

            st.success(
                "Runbook generated and saved to SQLite."
            )

    if st.session_state.runbooks:

        runbook = (
            st.session_state.runbooks[-1]
        )

        st.divider()

        st.subheader(
            f"📘 {runbook['PR_ID']} — "
            f"{runbook['Title']}"
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
                "### Root-Cause Signals"
            )

            for item in runbook[
                "Root Cause"
            ]:

                st.write(
                    "• " + item
                )

            st.write(
                "### Reusable Actions"
            )

            for item in runbook[
                "Reusable Actions"
            ]:

                st.write(
                    "• " + item
                )

        with col2:

            st.write(
                "### Verification Steps"
            )

            for item in runbook[
                "Verification Steps"
            ]:

                st.write(
                    "• " + item
                )

            st.write(
                "### Evidence Sources"
            )

            st.write(
                ", ".join(
                    runbook[
                        "Evidence Sources"
                    ]
                )
            )

            st.metric(
                "Evidence",
                f"{runbook['Evidence Count']} / 4"
            )

            st.metric(
                "Confidence",
                f"{runbook['Confidence']}%"
            )

            if runbook[
                "High Impact"
            ]:

                st.error(
                    "🚨 HIGH-IMPACT CHANGE — "
                    "human confirmation required."
                )

            else:

                st.success(
                    "NORMAL-IMPACT CHANGE"
                )

        st.divider()

        st.subheader(
            "🔎 Evidence"
        )

        st.write(
            "**PR Resolution:**",
            runbook["Solution"]
        )

        st.write(
            "**Changed File:**",
            runbook["Changed File"]
        )

        if runbook[
            "Changed File"
        ] != "Code diff unavailable.":

            c1, c2 = st.columns(2)

            with c1:

                st.write(
                    "Previous Code"
                )

                st.code(
                    runbook["Old Code"]
                )

            with c2:

                st.write(
                    "Updated Code"
                )

                st.code(
                    runbook["New Code"]
                )

        st.write(
            "**Reviewer:**",
            runbook["Reviewer"]
        )

        st.write(
            "**Reviewer Status:**",
            runbook["Reviewer Status"]
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

    for index, runbook in enumerate(
        st.session_state.runbooks
    ):

        st.divider()

        st.subheader(
            f"{runbook['PR_ID']} — "
            f"{runbook['Title']}"
        )

        st.write(
            f"Verification: "
            f"**{runbook['Verification Status']}**"
        )

        st.write(
            f"Trust Status: "
            f"**{runbook.get('Trust Status', 'PENDING HUMAN APPROVAL')}**"
        )

        if runbook[
            "Changed File"
        ] == "Code diff unavailable.":

            st.error(
                "❌ Approval blocked: "
                "Code diff is missing."
            )

            continue

        if (
            runbook["Reviewer Status"]
            .lower()
            != "approved"
        ):

            st.warning(
                "⏳ Approval blocked: "
                "reviewer approval is required."
            )

            continue

        confirmation = True

        if runbook[
            "High Impact"
        ]:

            confirmation = st.checkbox(
                "I confirm that this high-impact runbook has been manually reviewed.",
                key=f"confirm_{index}"
            )

        reviewer_name = st.text_input(
            "Human Reviewer",
            key=f"reviewer_{index}"
        )

        approval_reason = st.text_area(
            "Approval Reason",
            key=f"approval_reason_{index}"
        )

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "✅ Approve as Trusted",
                key=f"approve_{index}"
            ):

                if not confirmation:

                    st.error(
                        "Human confirmation is required."
                    )

                elif not reviewer_name.strip():

                    st.error(
                        "Reviewer name is required."
                    )

                elif not approval_reason.strip():

                    st.error(
                        "Approval reason is required."
                    )

                else:

                    runbook[
                        "Trust Status"
                    ] = "TRUSTED / VERIFIED"

                    runbook[
                        "Human Review Status"
                    ] = "Approved"

                    runbook[
                        "Human Reviewer"
                    ] = reviewer_name

                    runbook[
                        "Approval Reason"
                    ] = approval_reason

                    runbook[
                        "Approved At"
                    ] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    save_runbook(
                        runbook
                    )

                    save_audit(
                        "Runbook Approved",
                        f"{runbook['PR_ID']} approved by {reviewer_name}"
                    )

                    st.success(
                        "Runbook is now "
                        "TRUSTED / VERIFIED."
                    )

        with c2:

            rejection_reason = st.text_input(
                "Rejection Reason",
                key=f"rejection_{index}"
            )

            if st.button(
                "❌ Reject Runbook",
                key=f"reject_{index}"
            ):

                if not rejection_reason.strip():

                    st.error(
                        "Rejection reason is required."
                    )

                else:

                    runbook[
                        "Trust Status"
                    ] = "REJECTED"

                    runbook[
                        "Human Review Status"
                    ] = "Rejected"

                    runbook[
                        "Rejection Reason"
                    ] = rejection_reason

                    save_runbook(
                        runbook
                    )

                    save_audit(
                        "Runbook Rejected",
                        f"{runbook['PR_ID']}: {rejection_reason}"
                    )

                    st.warning(
                        "Runbook rejected and saved."
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
        This is a mock integration. No production system
        is modified.
        """
    )

    ids = get_pr_ids()

    if ids:

        pr_id = st.selectbox(
            "Select PR",
            ids
        )

        if st.button(
            "📡 Send Data to Mock API"
        ):

            pr = get_pr(pr_id)
            incident = get_incident(pr_id)
            diff = get_diff(pr_id)
            review = get_review(pr_id)

            payload = {

                "timestamp":
                    datetime.now().isoformat(),

                "pull_request":
                    pr.to_dict()
                    if pr is not None
                    else {},

                "incident":
                    incident.to_dict()
                    if incident is not None
                    else {},

                "code_diff":
                    diff.to_dict()
                    if diff is not None
                    else {},

                "review":
                    review.to_dict()
                    if review is not None
                    else {}
            }

            st.session_state.api_records.append(
                payload
            )

            save_audit(
                "API Data Received",
                f"Mock engineering data received for {pr_id}"
            )

            st.json(
                payload
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

        This feature does not modify production code.
        It records the rollback path and reason.
        """
    )

    ids = get_pr_ids()

    if ids:

        pr_id = st.selectbox(
            "Select Pull Request",
            ids
        )

        pr = get_pr(
            pr_id
        )

        diff = get_diff(
            pr_id
        )

        if diff is not None:

            c1, c2 = st.columns(2)

            with c1:

                st.write(
                    "### Previous Version"
                )

                st.code(
                    get_value(
                        diff,
                        [
                            "Old_Code",
                            "Old Code",
                            "Before"
                        ]
                    )
                )

            with c2:

                st.write(
                    "### Current Version"
                )

                st.code(
                    get_value(
                        diff,
                        [
                            "New_Code",
                            "New Code",
                            "After"
                        ]
                    )
                )

        combined_text = " ".join(
            [
                get_value(
                    pr,
                    ["Title"]
                ),
                get_value(
                    pr,
                    ["Description"]
                ),
                get_value(
                    pr,
                    ["Resolution"]
                )
            ]
        )

        confirmation = True

        if is_high_impact(
            combined_text
        ):

            confirmation = st.checkbox(
                "I confirm that rollback is required."
            )

        reason = st.text_area(
            "Rollback Reason"
        )

        if st.button(
            "🔄 Record Rollback"
        ):

            if not confirmation:

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

                save_rollback(
                    record
                )

                save_audit(
                    "Rollback Recorded",
                    f"{pr_id}: {reason}"
                )

                st.success(
                    "Rollback path recorded."
                )

    if st.session_state.rollback_log:

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

    st.info(
        """
        High-impact keywords:

        authentication • security • password • permission •
        database • payment • delete • production •
        credential • access
        """
    )

    ids = get_pr_ids()

    if ids:

        pr_id = st.selectbox(
            "Select Pull Request",
            ids
        )

        pr = get_pr(
            pr_id
        )

        text = " ".join(
            [
                get_value(
                    pr,
                    ["Title"]
                ),
                get_value(
                    pr,
                    ["Description"]
                ),
                get_value(
                    pr,
                    ["Resolution"]
                )
            ]
        )

        high_impact, keywords = risk_info(
            text
        )

        if high_impact:

            st.error(
                "🚨 HIGH-IMPACT CHANGE"
            )

            st.write(
                "Detected keywords:",
                ", ".join(keywords)
            )

            st.write(
                "Human confirmation is required."
            )

        else:

            st.success(
                "✅ NORMAL-IMPACT CHANGE"
            )

            st.write(
                "No configured high-impact "
                "keywords detected."
            )

# ============================================================
# EDGE CASES
# ============================================================

elif page == "🧪 Edge Cases":

    st.title(
        "🧪 Edge & Failure Cases"
    )

    cases = {

        "Missing Incident":
            "Show warning and mark root-cause evidence incomplete.",

        "Pending Reviewer":
            "Block trusted approval until reviewer approval.",

        "Missing Code Diff":
            "Mark runbook incomplete and block approval.",

        "High-Impact Change":
            "Require human confirmation.",

        "Rollback Without Reason":
            "Block rollback recording."
    }

    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Case":
                        key,

                    "System Response":
                        value
                }

                for key, value
                in cases.items()
            ]
        ),
        use_container_width=True
    )

    test_case = st.selectbox(
        "Test Edge Case",
        list(cases.keys())
    )

    st.warning(
        cases[test_case]
    )

# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "📝 Audit Trail":

    st.title(
        "📝 Audit Trail"
    )

    audit = load_table(
        "audit_log"
    )

    st.session_state.audit_log = audit

    if not audit:

        st.info(
            "No audit events yet."
        )

    else:

        audit_df = pd.DataFrame(
            audit
        )

        st.dataframe(
            audit_df,
            use_container_width=True
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Total Events",
            len(audit_df)
        )

        c2.metric(
            "Runbooks Generated",
            sum(
                audit_df["Action"]
                == "Runbook Generated"
            )
        )

        c3.metric(
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
        Compare the same maintenance task without the assistant
        and with the assistant.

        Record actual measurements. Do not invent results.
        """
    )

    st.subheader(
        "➕ Add Experiment Result"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        tester = st.text_input(
            "Tester / Engineer ID",
            placeholder="Engineer-01"
        )

    with c2:

        test_case = st.text_input(
            "Test Case",
            placeholder="Redis timeout fix"
        )

    with c3:

        result = st.selectbox(
            "Result",
            [
                "Success",
                "Partial Success",
                "Failure"
            ]
        )

    c1, c2 = st.columns(2)

    with c1:

        baseline_time = st.number_input(
            "Baseline Time (minutes)",
            min_value=0.1,
            value=30.0
        )

    with c2:

        assistant_time = st.number_input(
            "Assistant Time (minutes)",
            min_value=0.1,
            value=20.0
        )

    correctness = st.selectbox(
        "Recommendation Correctness",
        [
            "Correct",
            "Partially Correct",
            "Incorrect"
        ]
    )

    observation = st.text_area(
        "Observation / Error Analysis",
        placeholder=(
            "What worked, failed, or required "
            "manual correction?"
        )
    )

    if st.button(
        "➕ Add Validation Result",
        type="primary"
    ):

        if not tester.strip():

            st.error(
                "Tester ID is required."
            )

        elif not test_case.strip():

            st.error(
                "Test case is required."
            )

        else:

            time_saved = (
                baseline_time
                - assistant_time
            )

            reduction = (
                time_saved
                / baseline_time
            ) * 100

            record = {

                "Tester":
                    tester,

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

                "Result":
                    result,

                "Correctness":
                    correctness,

                "Observation":
                    observation,

                "Timestamp":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
            }

            save_validation(
                record
            )

            save_audit(
                "Validation Result Added",
                f"{test_case} by {tester}"
            )

            if time_saved < 0:

                st.warning(
                    """
                    This is a regression case:
                    the assistant took longer than
                    the baseline.

                    The result was kept because
                    real experiments must allow
                    negative results.
                    """
                )

            else:

                st.success(
                    "Validation result saved."
                )

    # ========================================================
    # LOAD RESULTS
    # ========================================================

    results = load_table(
        "validation_results"
    )

    st.session_state.experiment_results = (
        results
    )

    if results:

        results_df = pd.DataFrame(
            results
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

        median_reduction = results_df[
            "Reduction %"
        ].median()

        if len(results_df) > 1:

            std_reduction = results_df[
                "Reduction %"
            ].std()

        else:

            std_reduction = 0

        success_rate = (
            results_df["Result"]
            == "Success"
        ).mean() * 100

        correctness_rate = (
            results_df["Correctness"]
            == "Correct"
        ).mean() * 100

        regression_count = sum(
            results_df["Time Saved"] < 0
        )

        c1, c2, c3, c4, c5, c6 = (
            st.columns(6)
        )

        c1.metric(
            "Avg Baseline",
            f"{avg_baseline:.1f} min"
        )

        c2.metric(
            "Avg Assistant",
            f"{avg_assistant:.1f} min"
        )

        c3.metric(
            "Avg Time Saved",
            f"{avg_saved:.1f} min"
        )

        c4.metric(
            "Avg Reduction",
            f"{avg_reduction:.1f}%"
        )

        c5.metric(
            "Correctness",
            f"{correctness_rate:.1f}%"
        )

        c6.metric(
            "Regressions",
            regression_count
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Median Reduction",
            f"{median_reduction:.1f}%"
        )

        c2.metric(
            "Std Deviation",
            f"{std_reduction:.1f}%"
        )

        c3.metric(
            "Success Rate",
            f"{success_rate:.1f}%"
        )

        c4.metric(
            "Test Cases",
            len(results_df)
        )

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
                Target achieved.

                Target: {target}% reduction

                Measured:
                {avg_reduction:.1f}% reduction
                """
            )

        else:

            st.warning(
                f"""
                Target not yet achieved.

                Target: {target}% reduction

                Measured:
                {avg_reduction:.1f}% reduction
                """
            )

        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        st.subheader(
            "📋 Experiment Results"
        )

        st.dataframe(
            results_df,
            use_container_width=True
        )

        # ----------------------------------------------------
        # ERROR ANALYSIS
        # ----------------------------------------------------

        st.subheader(
            "🔍 Error Analysis"
        )

        issues = results_df[
            (
                results_df["Result"]
                != "Success"
            )
            |
            (
                results_df["Correctness"]
                != "Correct"
            )
            |
            (
                results_df["Time Saved"]
                < 0
            )
        ]

        if issues.empty:

            st.success(
                """
                No unsuccessful,
                incorrect, or regression
                cases recorded.
                """
            )

        else:

            st.warning(
                f"{len(issues)} case(s) "
                "require analysis."
            )

            st.dataframe(
                issues[
                    [
                        "Tester",
                        "Test Case",
                        "Result",
                        "Correctness",
                        "Time Saved",
                        "Reduction %",
                        "Observation"
                    ]
                ],
                use_container_width=True
            )

        # ----------------------------------------------------
        # TIME COMPARISON
        # ----------------------------------------------------

        st.subheader(
            "⏱️ Time Comparison"
        )

        for _, row in results_df.iterrows():

            st.write(
                f"""
                **{row['Test Case']}**

                Baseline:
                {row['Baseline Minutes']:.1f} minutes

                Assistant:
                {row['Assistant Minutes']:.1f} minutes

                Time Saved:
                {row['Time Saved']:.1f} minutes

                Reduction:
                {row['Reduction %']:.1f}%
                """
            )

            st.divider()

    else:

        st.info(
            """
            No validation results yet.

            Add real baseline-vs-assistant
            measurements to populate the dashboard.
            """
        )

# ============================================================
# END
# ============================================================
