import streamlit as st
import pandas as pd
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
# HELPER FUNCTIONS
# ============================================================

def add_audit(action, details):

    st.session_state.audit_log.append(
        {
            "Timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "Action":
                action,

            "Details":
                details
        }
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
                f"{runbook['PR_ID']} - "
                f"{runbook['Title']}"
            )

            st.write(
                f"Confidence: "
                f"**{runbook['Confidence']}%**"
            )

            st.write(
                f"Verification: "
                f"**{runbook['Verification Status']}**"
            )

            if (
                runbook["Changed File"]
                == "Code diff unavailable."
            ):

                st.error(
                    "❌ Approval blocked: Code diff is missing."
                )

                continue

            if (
                runbook["Reviewer Status"]
                .lower()
                != "approved"
            ):

                st.warning(
                    "⏳ Approval blocked: Reviewer approval is required."
                )

                continue

            confirmation = True

            if runbook["High Impact"]:

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

        elif assistant_time > baseline_time:

            st.error(
                "Assistant time cannot be greater than baseline time."
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

                "Result":
                    result,

                "Observation":
                    observation
            }

            st.session_state.experiment_results.append(
                experiment
            )

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

        success_rate = (
            results_df["Result"]
            == "Success"
        ).mean() * 100

        col1, col2, col3, col4, col5 = st.columns(5)

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
