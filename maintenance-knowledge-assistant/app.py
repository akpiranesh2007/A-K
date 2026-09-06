import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Maintenance Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM THEME
# Dark Purple + Cyan
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #0F1020;
        color: #F5F5F7;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #17182B;
        border-right: 1px solid #303252;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: #F5F5F7;
    }

    /* Main headings */
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

    /* Normal text */
    p, label {
        color: #E5E7EB !important;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #191B32;
        border: 1px solid #34365A;
        border-radius: 14px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }

    div[data-testid="metric-container"] label {
        color: #A5B4FC !important;
    }

    div[data-testid="metric-container"] div {
        color: #67E8F9 !important;
    }

    /* Buttons */
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

    /* Info boxes */
    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border: 1px solid #34365A;
        border-radius: 12px;
    }

    /* Text inputs */
    input, textarea {
        background-color: #191B32 !important;
        color: white !important;
        border: 1px solid #3B3D66 !important;
        border-radius: 8px !important;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #191B32;
        border: 1px solid #3B3D66;
        border-radius: 8px;
    }

    /* Code */
    code {
        color: #67E8F9 !important;
    }

    /* Divider */
    hr {
        border-color: #303252;
    }

    /* Custom project banner */
    .project-banner {
        background: linear-gradient(
            135deg,
            #312E81,
            #4C1D95,
            #155E75
        );
        padding: 25px;
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

    /* Status card */
    .status-card {
        background-color: #191B32;
        border: 1px solid #34365A;
        padding: 18px;
        border-radius: 14px;
        margin-top: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA PATH
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

    st.error("Unable to load project data.")

    st.code("""
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
""")

    st.error(str(e))
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


# ============================================================
# AUDIT
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
# RISK CHECK
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
        word in text
        for word in keywords
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


    # Incident
    if len(incident_rows) == 0:

        incident_problem = "Incident information is missing."

        incident_discussion = (
            "Root cause cannot be fully verified."
        )

        incident_available = False

    else:

        incident = incident_rows.iloc[0]

        incident_problem = incident["Problem"]

        incident_discussion = incident["Discussion"]

        incident_available = True


    # Code diff
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


    # Review
    if len(review_rows) == 0:

        reviewer_status = "Unknown"

        verification = (
            "Reviewer information unavailable."
        )

    else:

        review = review_rows.iloc[0]

        reviewer_status = review["Decision"]

        verification = review["Comment"]


    # Confidence
    confidence = 40

    if incident_available:
        confidence += 15

    if diff_available:
        confidence += 15

    if reviewer_status == "Approved":
        confidence += 30

    confidence = min(confidence, 100)


    # Verification
    if not incident_available:

        verification_status = (
            "Incomplete - Incident missing"
        )

    elif not diff_available:

        verification_status = (
            "Incomplete - Code diff missing"
        )

    elif reviewer_status != "Approved":

        verification_status = (
            "Pending - Reviewer approval required"
        )

    else:

        verification_status = "Verified"


    high_impact = is_high_impact(
        pr["Title"]
        + " "
        + pr["Description"]
        + " "
        + pr["Resolution"]
    )


    return {

        "PR_ID": pr_id,

        "Title": pr["Title"],

        "Problem": incident_problem,

        "Root_Cause": incident_discussion,

        "Solution": pr["Resolution"],

        "Changed_File": changed_file,

        "Old_Code": old_code,

        "New_Code": new_code,

        "Verification": verification,

        "Reviewer_Status": reviewer_status,

        "Verification_Status": verification_status,

        "Confidence": confidence,

        "High_Impact": high_impact,

        "Incident_Available": incident_available,

        "Diff_Available": diff_available
    }


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <h2 style="color:#67E8F9;">🧠 MKA</h2>
    <p style="color:#A5B4FC;">
    Maintenance Knowledge Assistant
    </p>
    """,
    unsafe_allow_html=True
)


page = st.sidebar.radio(

    "MENU",

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
    "Synthetic / Anonymised Dataset"
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="project-banner">

        <h1>🧠 Maintenance Knowledge-Capture Assistant</h1>

        <p>
        Convert completed software fixes into verified,
        reusable maintenance knowledge.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Pull Requests",
        len(pull_requests)
    )

    col2.metric(
        "Incidents",
        len(incidents)
    )

    col3.metric(
        "Runbooks",
        len(st.session_state.runbooks)
    )

    col4.metric(
        "Audit Events",
        len(st.session_state.audit_log)
    )


    st.divider()


    st.subheader(
        "🔄 Knowledge Capture Workflow"
    )

    st.info(
        """
        Completed Fix
        ↓
        Pull Request
        ↓
        Incident Discussion
        ↓
        Code Diff
        ↓
        Reviewer Approval
        ↓
        Runbook Generation
        ↓
        Human Verification
        ↓
        Reusable Knowledge
        """
    )


    st.subheader(
        "🎯 Project Objective"
    )

    st.write(
        "Reduce the time required for a new engineer "
        "to repeat a known software fix."
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
        "PR Details"
    )

    selected_pr = st.selectbox(
        "Select Pull Request",
        pull_requests["PR_ID"].tolist()
    )

    pr = pull_requests[
        pull_requests["PR_ID"] == selected_pr
    ].iloc[0]


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


    st.write(
        "### Reviewer"
    )

    st.write(
        pr["Reviewer"]
    )


    st.write(
        "### Status"
    )

    st.write(
        pr["Status"]
    )


# ============================================================
# INCIDENTS
# ============================================================

elif page == "🚨 Incidents":

    st.title(
        "🚨 Incident Records"
    )

    st.dataframe(
        incidents,
        use_container_width=True
    )


    selected_incident = st.selectbox(
        "Select Incident",
        incidents["Incident_ID"].tolist()
    )

    incident = incidents[
        incidents["Incident_ID"]
        == selected_incident
    ].iloc[0]


    st.write(
        "### Problem"
    )

    st.write(
        incident["Problem"]
    )


    st.write(
        "### Team Discussion"
    )

    st.write(
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

    selected_pr = st.selectbox(
        "Select Pull Request",
        pull_requests["PR_ID"].tolist()
    )


    if st.button(
        "🚀 Generate Runbook"
    ):

        runbook = generate_runbook(
            selected_pr
        )


        if "error" in runbook:

            st.error(
                runbook["error"]
            )

        else:

            st.session_state.runbooks.append(
                runbook
            )

            add_audit(

                "Runbook Generated",

                selected_pr,

                "Runbook generated from available evidence."

            )

            st.success(
                "✅ Runbook generated successfully."
            )


    if st.session_state.runbooks:

        rb = st.session_state.runbooks[-1]

        st.divider()

        st.subheader(
            "📘 Generated Runbook"
        )


        st.write(
            "### Problem"
        )

        st.write(
            rb["Problem"]
        )


        st.write(
            "### Root Cause"
        )

        st.write(
            rb["Root_Cause"]
        )


        st.write(
            "### Solution"
        )

        st.success(
            rb["Solution"]
        )


        st.write(
            "### Changed File"
        )

        st.code(
            rb["Changed_File"]
        )


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                "### Previous Code"
            )

            st.code(
                rb["Old_Code"]
            )


        with col2:

            st.write(
                "### New Code"
            )

            st.code(
                rb["New_Code"]
            )


        col1, col2 = st.columns(2)


        col1.metric(
            "Confidence",
            f'{rb["Confidence"]}%'
        )

        col2.metric(
            "Verification",
            rb["Verification_Status"]
        )


        if not rb["Incident_Available"]:

            st.warning(
                "⚠️ Incident evidence is missing."
            )


        if not rb["Diff_Available"]:

            st.warning(
                "⚠️ Code diff evidence is missing."
            )


        if rb["Reviewer_Status"] != "Approved":

            st.warning(
                "⏳ Reviewer approval is required."
            )


        if rb["High_Impact"]:

            st.error(
                "🚨 High-impact change detected."
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

        for i, rb in enumerate(
            st.session_state.runbooks
        ):

            st.divider()

            st.subheader(
                f'{rb["PR_ID"]} - {rb["Title"]}'
            )


            st.write(
                f'Confidence: {rb["Confidence"]}%'
            )


            if (
                not rb["Incident_Available"]
                or not rb["Diff_Available"]
            ):

                st.error(
                    "❌ Approval blocked because "
                    "required evidence is missing."
                )

                continue


            if rb["Reviewer_Status"] != "Approved":

                st.warning(
                    "⏳ Approval blocked until "
                    "reviewer approval is available."
                )

                continue


            if rb["High_Impact"]:

                confirmation = st.checkbox(

                    "I confirm this high-impact "
                    "runbook can be approved.",

                    key=f"confirm_{i}"

                )

            else:

                confirmation = True


            col1, col2 = st.columns(2)


            with col1:

                if st.button(
                    "✅ Approve",
                    key=f"approve_{i}"
                ):

                    if confirmation:

                        add_audit(

                            "Runbook Approved",

                            rb["PR_ID"],

                            "Human approval recorded."

                        )

                        st.success(
                            "Runbook approved."
                        )

                    else:

                        st.error(
                            "Human confirmation required."
                        )


            with col2:

                reason = st.text_input(

                    "Rejection reason",

                    key=f"reject_reason_{i}"

                )


                if st.button(

                    "❌ Reject",

                    key=f"reject_{i}"

                ):

                    if reason.strip():

                        add_audit(

                            "Runbook Rejected",

                            rb["PR_ID"],

                            reason

                        )

                        st.warning(
                            "Runbook rejected."
                        )

                    else:

                        st.error(
                            "Rejection reason required."
                        )


# ============================================================
# API INTEGRATION
# ============================================================

elif page == "🔌 API Integration":

    st.title(
        "🔌 API Integration"
    )

    st.write(
        "Mock API showing how an external engineering "
        "system can send maintenance information."
    )


    selected_pr = st.selectbox(

        "Select PR",

        pull_requests["PR_ID"].tolist()

    )


    if st.button(
        "📤 Send Data"
    ):

        pr = pull_requests[
            pull_requests["PR_ID"]
            == selected_pr
        ].iloc[0]


        incident_rows = incidents[
            incidents["PR_ID"]
            == selected_pr
        ]


        diff_rows = code_diffs[
            code_diffs["PR_ID"]
            == selected_pr
        ]


        review_rows = reviews[
            reviews["PR_ID"]
            == selected_pr
        ]


        payload = {

            "source":
                "Mock Engineering API",

            "timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "PR_ID":
                selected_pr,

            "title":
                pr["Title"],

            "description":
                pr["Description"],

            "resolution":
                pr["Resolution"],

            "incident":
                (
                    incident_rows.iloc[0].to_dict()
                    if len(incident_rows) > 0
                    else {}
                ),

            "code_diff":
                (
                    diff_rows.iloc[0].to_dict()
                    if len(diff_rows) > 0
                    else {}
                ),

            "review":
                (
                    review_rows.iloc[0].to_dict()
                    if len(review_rows) > 0
                    else {}
                )
        }


        st.session_state.api_records.append(
            payload
        )


        add_audit(

            "API Data Received",

            selected_pr,

            "Data received through mock API."

        )


        st.success(
            "✅ API data received successfully."
        )


        st.json(
            payload
        )


# ============================================================
# ROLLBACK
# ============================================================

elif page == "🔄 Rollback Manager":

    st.title(
        "🔄 Rollback Manager"
    )


    st.warning(
        "Prototype simulation — no real production code "
        "is modified."
    )


    selected_pr = st.selectbox(

        "Select PR",

        pull_requests["PR_ID"].tolist()

    )


    diff_rows = code_diffs[
        code_diffs["PR_ID"]
        == selected_pr
    ]


    if len(diff_rows) == 0:

        st.error(
            "❌ Code diff unavailable."
        )

    else:

        diff = diff_rows.iloc[0]

        pr = pull_requests[
            pull_requests["PR_ID"]
            == selected_pr
        ].iloc[0]


        high_impact = is_high_impact(

            pr["Title"]
            + " "
            + pr["Description"]

        )


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                "### Previous Safe Version"
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

            st.warning(
                "🚨 Human confirmation required."
            )

            confirmation = st.checkbox(
                "I confirm this rollback.",
                key=f"rollback_{selected_pr}"
            )

        else:

            confirmation = True


        reason = st.text_area(
            "Rollback Reason"
        )


        if st.button(
            "🔄 Confirm Rollback"
        ):

            if not reason.strip():

                st.error(
                    "❌ Rollback blocked: "
                    "reason required."
                )

            elif not confirmation:

                st.error(
                    "❌ Human confirmation required."
                )

            else:

                record = {

                    "Timestamp":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                    "PR_ID":
                        selected_pr,

                    "File":
                        diff["File"],

                    "Restored_To":
                        diff["Old_Code"],

                    "Reason":
                        reason,

                    "Status":
                        "Rollback Recorded"
                }


                st.session_state.rollback_log.append(
                    record
                )


                add_audit(

                    "Rollback Recorded",

                    selected_pr,

                    reason

                )


                st.success(
                    "✅ Rollback recorded."
                )


    if st.session_state.rollback_log:

        st.subheader(
            "📜 Rollback History"
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


    selected_pr = st.selectbox(

        "Select PR",

        pull_requests["PR_ID"].tolist()

    )


    pr = pull_requests[
        pull_requests["PR_ID"]
        == selected_pr
    ].iloc[0]


    text = (

        pr["Title"]
        + " "
        + pr["Description"]
        + " "
        + pr["Resolution"]

    )


    if is_high_impact(text):

        st.error(
            "🚨 HIGH-IMPACT CHANGE"
        )

        st.write(
            "Human confirmation is required."
        )

    else:

        st.success(
            "✅ Normal-risk change"
        )


# ============================================================
# EDGE CASES
# ============================================================

elif page == "🧪 Edge Cases":

    st.title(
        "🧪 Edge & Failure Cases"
    )


    edge_data = pd.DataFrame({

        "Edge Case": [

            "Missing Incident",

            "Pending Reviewer",

            "Missing Code Diff",

            "High-Impact Change",

            "Rollback Without Reason"

        ],

        "System Response": [

            "Warning",

            "Approval Blocked",

            "Incomplete Runbook",

            "Human Confirmation",

            "Rollback Blocked"

        ],

        "Status": [

            "Handled",

            "Handled",

            "Handled",

            "Handled",

            "Handled"

        ]

    })


    st.dataframe(

        edge_data,

        use_container_width=True

    )


    st.success(
        "✅ All required edge cases are handled."
    )


# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "📝 Audit Trail":

    st.title(
        "📝 Audit Trail"
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


        col1, col2, col3 = st.columns(3)


        col1.metric(

            "Total Events",

            len(audit_df)

        )


        col2.metric(

            "API Events",

            len(
                audit_df[
                    audit_df["Action"]
                    == "API Data Received"
                ]
            )

        )


        col3.metric(

            "Rollback Events",

            len(
                audit_df[
                    audit_df["Action"]
                    == "Rollback Recorded"
                ]
            )

        )


# ============================================================
# VALIDATION DASHBOARD
# ============================================================

elif page == "📊 Validation Dashboard":

    st.title(
        "📊 Validation & Metrics Dashboard"
    )


    st.write(
        "Measure whether the assistant reduces "
        "the time needed to repeat known fixes."
    )


    st.divider()


    # ========================================================
    # ADD TEST
    # ========================================================

    st.subheader(
        "1️⃣ Add Experiment Result"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        test_case = st.text_input(
            "Test Case",
            placeholder="Redis timeout fix"
        )


    with col2:

        baseline_time = st.number_input(

            "Without Assistant (minutes)",

            min_value=1.0,

            value=60.0,

            step=1.0

        )


    with col3:

        assistant_time = st.number_input(

            "With Assistant (minutes)",

            min_value=1.0,

            value=30.0,

            step=1.0

        )


    result_status = st.selectbox(

        "Result",

        [
            "Success",
            "Partial Success",
            "Failure"
        ]

    )


    observation = st.text_input(

        "Error / Observation",

        placeholder=(
            "Example: Engineer needed clarification."
        )

    )


    if st.button(
        "➕ Add Experiment"
    ):

        if not test_case.strip():

            st.error(
                "Please enter a test case."
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


            result = {

                "Test Case":
                    test_case,

                "Baseline (min)":
                    baseline_time,

                "Assistant (min)":
                    assistant_time,

                "Time Saved (min)":
                    round(
                        time_saved,
                        2
                    ),

                "Reduction (%)":
                    round(
                        reduction,
                        2
                    ),

                "Result":
                    result_status,

                "Observation":
                    observation
            }


            st.session_state.experiment_results.append(
                result
            )


            add_audit(

                "Experiment Added",

                "N/A",

                test_case

            )


            st.success(
                "✅ Experiment added."
            )


    # ========================================================
    # RESULTS
    # ========================================================

    if st.session_state.experiment_results:

        st.divider()

        st.subheader(
            "2️⃣ Experiment Results"
        )


        results_df = pd.DataFrame(

            st.session_state.experiment_results

        )


        st.dataframe(

            results_df,

            use_container_width=True

        )


        # ====================================================
        # METRICS
        # ====================================================

        st.subheader(
            "3️⃣ Key Performance Metrics"
        )


        avg_baseline = results_df[
            "Baseline (min)"
        ].mean()


        avg_assistant = results_df[
            "Assistant (min)"
        ].mean()


        avg_saved = results_df[
            "Time Saved (min)"
        ].mean()


        avg_reduction = results_df[
            "Reduction (%)"
        ].mean()


        success_count = len(

            results_df[
                results_df["Result"]
                == "Success"
            ]

        )


        total_tests = len(
            results_df
        )


        success_rate = (

            success_count
            / total_tests

        ) * 100


        col1, col2, col3, col4 = st.columns(4)


        col1.metric(

            "Avg. Baseline",

            f"{avg_baseline:.1f} min"

        )


        col2.metric(

            "Avg. Assistant",

            f"{avg_assistant:.1f} min"

        )


        col3.metric(

            "Avg. Time Saved",

            f"{avg_saved:.1f} min"

        )


        col4.metric(

            "Avg. Reduction",

            f"{avg_reduction:.1f}%"

        )


        st.metric(

            "Success Rate",

            f"{success_rate:.1f}%"

        )


        # ====================================================
        # CHART
        # ====================================================

        st.subheader(
            "4️⃣ Baseline vs Assistant"
        )


        chart_data = results_df[
            [
                "Test Case",
                "Baseline (min)",
                "Assistant (min)"
            ]
        ].set_index(
            "Test Case"
        )


        st.bar_chart(
            chart_data
        )


        # ====================================================
        # ERROR ANALYSIS
        # ====================================================

        st.subheader(
            "5️⃣ Error Analysis"
        )


        failures = results_df[
            results_df["Result"]
            != "Success"
        ]


        if len(failures) == 0:

            st.success(
                "✅ No failed test cases."
            )

        else:

            st.warning(

                f"{len(failures)} "
                "test case(s) need analysis."

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


        # ====================================================
        # TARGET
        # ====================================================

        st.subheader(
            "6️⃣ Project Target"
        )


        target = 30


        st.write(
            "Target: At least 30% reduction "
            "in known-fix reproduction time."
        )


        if avg_reduction >= target:

            st.success(

                f"🎯 Target achieved: "
                f"{avg_reduction:.1f}% reduction."

            )

        else:

            st.warning(

                f"Target not yet achieved. "
                f"Current reduction: "
                f"{avg_reduction:.1f}%."

            )


        # ====================================================
        # CONCLUSION
        # ====================================================

        st.subheader(
            "7️⃣ Validation Conclusion"
        )


        st.info(

            f"""
Test cases completed: {total_tests}

Average baseline time:
{avg_baseline:.1f} minutes

Average assistant time:
{avg_assistant:.1f} minutes

Average time saved:
{avg_saved:.1f} minutes

Average time reduction:
{avg_reduction:.1f}%

Success rate:
{success_rate:.1f}%
"""

        )

    else:

        st.info(

            "Add experiment results above to "
            "generate your metrics dashboard."

        )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "🧠 MKA Prototype"
)

st.sidebar.caption(
    "Synthetic / Anonymised Data"
)
