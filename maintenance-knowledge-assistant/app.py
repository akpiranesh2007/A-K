import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Maintenance Knowledge Assistant",
    page_icon="🛠️",
    layout="wide"
)


# ============================================================
# DATA LOADING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


@st.cache_data
def load_data():

    pull_requests = pd.read_csv(DATA_DIR / "pull_requests.csv")
    incidents = pd.read_csv(DATA_DIR / "incidents.csv")
    code_diffs = pd.read_csv(DATA_DIR / "code_diffs.csv")
    reviews = pd.read_csv(DATA_DIR / "reviews.csv")

    return pull_requests, incidents, code_diffs, reviews


try:

    pull_requests, incidents, code_diffs, reviews = load_data()

except Exception as e:

    st.error("❌ Unable to load the data files.")

    st.write("Expected folder structure:")

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


# ============================================================
# AUDIT FUNCTION
# ============================================================

def add_audit(action, pr_id, details):

    st.session_state.audit_log.append({

        "Timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "Action": action,

        "PR_ID": pr_id,

        "Details": details
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

    # EDGE CASE 1:
    # PR does not exist

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


    # ========================================================
    # EDGE CASE 2:
    # MISSING INCIDENT
    # ========================================================

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


    # ========================================================
    # EDGE CASE 3:
    # MISSING CODE DIFF
    # ========================================================

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


    # ========================================================
    # REVIEW STATUS
    # ========================================================

    if len(review_rows) == 0:

        reviewer_status = "Unknown"

        verification = "Reviewer information unavailable."

    else:

        review = review_rows.iloc[0]

        reviewer_status = review["Decision"]

        verification = review["Comment"]


    # ========================================================
    # CONFIDENCE SCORE
    # ========================================================

    confidence = 40

    if incident_available:

        confidence += 15

    if diff_available:

        confidence += 15

    if reviewer_status == "Approved":

        confidence += 30

    confidence = min(
        confidence,
        100
    )


    # ========================================================
    # VERIFICATION STATUS
    # ========================================================

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


    # ========================================================
    # HIGH IMPACT
    # ========================================================

    high_impact = is_high_impact(

        pr["Title"]
        + " "
        + pr["Description"]
        + " "
        + pr["Resolution"]

    )


    # ========================================================
    # CREATE RUNBOOK
    # ========================================================

    runbook = {

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


    return runbook


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🛠️ Maintenance Assistant"
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

        "📊 Experiment"

    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title(
        "🛠️ Maintenance Knowledge-Capture Assistant"
    )

    st.write(
        "Convert completed software fixes into "
        "verified and reusable runbooks."
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
        "Generated Runbooks",
        len(st.session_state.runbooks)
    )

    col4.metric(
        "Audit Events",
        len(st.session_state.audit_log)
    )

    st.divider()

    st.subheader(
        "🔄 System Workflow"
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
Verified Knowledge
"""
    )

    st.subheader(
        "🎯 Project Goal"
    )

    st.write(
        "Reduce the time required for a new engineer "
        "to repeat a known fix."
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

    selected_pr = st.selectbox(

        "Select PR",

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

                "Runbook created from available PR, "
                "incident, code diff and review data."

            )

            st.success(
                "✅ Runbook generated successfully!"
            )


    if st.session_state.runbooks:

        st.divider()

        st.subheader(
            "Latest Runbook"
        )

        rb = st.session_state.runbooks[-1]

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

        st.write(
            "### Previous Code"
        )

        st.code(
            rb["Old_Code"]
        )

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


        # ====================================================
        # FAILURE WARNINGS
        # ====================================================

        if not rb["Incident_Available"]:

            st.warning(
                "⚠️ Edge Case: Incident data is missing."
            )

        if not rb["Diff_Available"]:

            st.warning(
                "⚠️ Edge Case: Code diff is missing."
            )

        if rb["Reviewer_Status"] != "Approved":

            st.warning(
                "⚠️ Reviewer approval is still required."
            )

        if rb["High_Impact"]:

            st.warning(
                "🚨 High-impact change detected. "
                "Human confirmation is required."
            )


# ============================================================
# REVIEW RUNBOOKS
# ============================================================

elif page == "✅ Review Runbooks":

    st.title(
        "✅ Review Runbooks"
    )

    if not st.session_state.runbooks:

        st.info(
            "No runbooks available. "
            "Generate a runbook first."
        )

    else:

        for i, rb in enumerate(
            st.session_state.runbooks
        ):

            st.divider()

            st.subheader(

                f'{rb["PR_ID"]} - '
                f'{rb["Title"]}'

            )

            st.write(
                f'**Confidence:** '
                f'{rb["Confidence"]}%'
            )

            st.write(
                f'**Status:** '
                f'{rb["Verification_Status"]}'
            )


            # Missing data means cannot be verified

            if (
                not rb["Incident_Available"]
                or not rb["Diff_Available"]
            ):

                st.error(
                    "❌ This runbook cannot be fully verified "
                    "because required evidence is missing."
                )

                continue


            # Pending review

            if rb["Reviewer_Status"] != "Approved":

                st.warning(
                    "⏳ Reviewer approval is required "
                    "before this runbook can be approved."
                )

                continue


            # High impact

            if rb["High_Impact"]:

                st.warning(
                    "🚨 High-impact action detected."
                )

                confirmation = st.checkbox(

                    "I confirm this high-impact runbook "
                    "can be approved.",

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

                            "Human reviewer approved the runbook."

                        )

                        st.success(
                            "Runbook approved."
                        )

                    else:

                        st.error(
                            "Human confirmation is required."
                        )


            with col2:

                reason = st.text_input(

                    "Rejection reason",

                    key=f"reason_{i}"

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
                            "Runbook rejected and "
                            "reason recorded."
                        )

                    else:

                        st.error(
                            "Please provide a rejection reason."
                        )


# ============================================================
# API INTEGRATION
# ============================================================

elif page == "🔌 API Integration":

    st.title(
        "🔌 API Integration"
    )

    st.write(
        "This prototype simulates how an external "
        "engineering system sends maintenance data "
        "to the assistant."
    )

    st.subheader(
        "📡 Mock API"
    )

    selected_pr = st.selectbox(

        "Select PR to send",

        pull_requests["PR_ID"].tolist()
    )

    if st.button(
        "📤 Send PR to Assistant"
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

            "Maintenance data received "
            "through mock API."

        )


        st.success(
            "✅ Data successfully received."
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

    st.write(
        "Record a rollback to the previous safe "
        "version of a change."
    )

    st.warning(
        "⚠️ This is a prototype simulation. "
        "It does not modify real production code."
    )

    st.divider()

    selected_pr = st.selectbox(

        "Select PR for rollback",

        pull_requests["PR_ID"].tolist()
    )

    diff_rows = code_diffs[
        code_diffs["PR_ID"]
        == selected_pr
    ]

    if len(diff_rows) == 0:

        st.error(
            "❌ No code diff found."
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


        st.subheader(
            "📂 Change Information"
        )

        st.write(
            f"**Pull Request:** {selected_pr}"
        )

        st.write(
            f"**File:** {diff['File']}"
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
                "🚨 HIGH-IMPACT CHANGE: "
                "Human confirmation is required."
            )

            human_confirmation = st.checkbox(

                "I confirm this rollback action.",

                key=f"rollback_confirm_{selected_pr}"

            )

        else:

            human_confirmation = True


        rollback_reason = st.text_area(

            "Rollback reason",

            placeholder=(
                "Example: The new change caused "
                "unexpected behaviour."
            )

        )


        if st.button(
            "🔄 Confirm Rollback"
        ):


            # EDGE CASE:
            # Missing rollback reason

            if not rollback_reason.strip():

                st.error(
                    "❌ Rollback blocked: "
                    "reason is required."
                )


            # EDGE CASE:
            # Missing human confirmation

            elif not human_confirmation:

                st.error(
                    "❌ Rollback blocked: "
                    "human confirmation is required."
                )


            else:

                rollback_record = {

                    "Timestamp":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                    "PR_ID":
                        selected_pr,

                    "File":
                        diff["File"],

                    "Rolled_Back_From":
                        diff["New_Code"],

                    "Restored_To":
                        diff["Old_Code"],

                    "Reason":
                        rollback_reason,

                    "Human_Confirmed":
                        True,

                    "Status":
                        "Rollback Recorded"
                }


                st.session_state.rollback_log.append(
                    rollback_record
                )


                add_audit(

                    "Rollback Recorded",

                    selected_pr,

                    f"Rollback reason: "
                    f"{rollback_reason}"

                )


                st.success(
                    "✅ Rollback recorded successfully."
                )


                st.info(
                    "No real source code was changed."
                )


    if st.session_state.rollback_log:

        st.divider()

        st.subheader(
            "📜 Rollback History"
        )

        rollback_df = pd.DataFrame(
            st.session_state.rollback_log
        )

        st.dataframe(
            rollback_df,
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
            "🚨 HIGH-IMPACT ACTION DETECTED"
        )

        st.write(
            "Human confirmation is required."
        )

    else:

        st.success(
            "✅ Normal-risk change"
        )

        st.write(
            "Standard review process can be followed."
        )


# ============================================================
# EDGE CASES
# ============================================================

elif page == "🧪 Edge Cases":

    st.title(
        "🧪 Edge & Failure Cases"
    )

    st.write(
        "The prototype tests how the assistant behaves "
        "when important information or approval is missing."
    )


    # ========================================================
    # CASE 1
    # ========================================================

    st.subheader(
        "1️⃣ Missing Incident Data"
    )

    st.write(
        "Expected behavior: The system should not crash."
    )

    st.info(
        "The runbook should show that incident evidence "
        "is missing and mark the runbook as incomplete."
    )


    # ========================================================
    # CASE 2
    # ========================================================

    st.subheader(
        "2️⃣ Pending Reviewer Approval"
    )

    st.write(
        "Expected behavior: The system should not "
        "automatically approve the runbook."
    )

    st.warning(
        "Human reviewer approval is required."
    )


    # ========================================================
    # CASE 3
    # ========================================================

    st.subheader(
        "3️⃣ Missing Code Diff"
    )

    st.write(
        "Expected behavior: The system should generate "
        "an incomplete runbook instead of pretending "
        "the evidence exists."
    )

    st.warning(
        "Code verification is incomplete."
    )


    # ========================================================
    # CASE 4
    # ========================================================

    st.subheader(
        "4️⃣ High-Impact Change"
    )

    st.write(
        "Expected behavior: A human must confirm the action."
    )

    st.error(
        "🚨 High-impact actions require human confirmation."
    )


    # ========================================================
    # CASE 5
    # ========================================================

    st.subheader(
        "5️⃣ Rollback Without Reason"
    )

    st.write(
        "Expected behavior: Rollback should be blocked "
        "until a reason is provided."
    )

    st.error(
        "❌ Rollback without a reason is blocked."
    )


    st.divider()

    st.subheader(
        "📊 Edge Case Summary"
    )

    edge_data = pd.DataFrame({

        "Edge Case": [

            "Missing Incident",

            "Pending Review",

            "Missing Code Diff",

            "High-Impact Action",

            "Rollback Without Reason"

        ],

        "System Response": [

            "Warning",

            "Approval Required",

            "Incomplete Runbook",

            "Human Confirmation",

            "Action Blocked"

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


# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "📝 Audit Trail":

    st.title(
        "📝 Complete Audit Trail"
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
            "🔍 Audit Summary"
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
# EXPERIMENT
# ============================================================

elif page == "📊 Experiment":

    st.title(
        "📊 Validation Experiment"
    )

    st.write(
        "Measure whether the assistant reduces "
        "the time required to repeat a known fix."
    )

    st.subheader(
        "⏱️ Enter Experiment Times"
    )


    baseline = st.number_input(

        "Baseline time without assistant (minutes)",

        min_value=1.0,

        value=60.0

    )


    assistant_time = st.number_input(

        "Time with assistant (minutes)",

        min_value=1.0,

        value=30.0

    )


    if st.button(
        "📈 Calculate Result"
    ):

        reduction = (

            (baseline - assistant_time)
            / baseline

        ) * 100


        st.success(

            f"Time reduction: "
            f"{reduction:.2f}%"

        )


        col1, col2, col3 = st.columns(3)


        col1.metric(

            "Baseline",

            f"{baseline:.1f} min"

        )


        col2.metric(

            "With Assistant",

            f"{assistant_time:.1f} min"

        )


        col3.metric(

            "Reduction",

            f"{reduction:.2f}%"

        )


        if reduction > 0:

            st.success(
                "The assistant reduced the time "
                "required to repeat the fix."
            )

        else:

            st.warning(
                "The assistant did not reduce "
                "the measured time."
            )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "Maintenance Knowledge-Capture Assistant"
)

st.sidebar.caption(
    "Prototype using synthetic/anonymised data"
)
