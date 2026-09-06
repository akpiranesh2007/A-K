import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Maintenance Knowledge Assistant",
    page_icon="🛠️",
    layout="wide"
)


# ============================================================
# LOAD CSV DATA
# ============================================================

@st.cache_data
def load_data():

    # Find the folder where app.py is located
    base_dir = Path(__file__).resolve().parent

    # data folder is beside app.py
    data_dir = base_dir / "data"

    # Read CSV files
    pull_requests = pd.read_csv(
        data_dir / "pull_requests.csv"
    )

    incidents = pd.read_csv(
        data_dir / "incidents.csv"
    )

    code_diffs = pd.read_csv(
        data_dir / "code_diffs.csv"
    )

    reviews = pd.read_csv(
        data_dir / "reviews.csv"
    )

    return (
        pull_requests,
        incidents,
        code_diffs,
        reviews
    )


# ============================================================
# LOAD DATA WITH ERROR MESSAGE
# ============================================================

try:

    (
        pull_requests,
        incidents,
        code_diffs,
        reviews
    ) = load_data()

except Exception as e:

    st.error("❌ Could not load the project data.")

    st.write(
        "Please make sure the GitHub project has this structure:"
    )

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

    st.error(f"Error details: {e}")

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "runbooks" not in st.session_state:
    st.session_state.runbooks = []

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_pr(pr_id):

    result = pull_requests[
        pull_requests["PR_ID"] == pr_id
    ]

    if len(result) == 0:
        return None

    return result.iloc[0]


def get_incident(pr_id):

    result = incidents[
        incidents["PR_ID"] == pr_id
    ]

    if len(result) == 0:
        return None

    return result.iloc[0]


def get_diff(pr_id):

    result = code_diffs[
        code_diffs["PR_ID"] == pr_id
    ]

    if len(result) == 0:
        return None

    return result.iloc[0]


def get_review(pr_id):

    result = reviews[
        reviews["PR_ID"] == pr_id
    ]

    if len(result) == 0:
        return None

    return result.iloc[0]


# ============================================================
# HIGH IMPACT CHECK
# ============================================================

def check_high_impact(text):

    keywords = [
        "security",
        "authentication",
        "database",
        "payment",
        "delete",
        "production",
        "password"
    ]

    text = str(text).lower()

    found_keywords = []

    for keyword in keywords:

        if keyword in text:
            found_keywords.append(keyword)

    return found_keywords


# ============================================================
# CONFIDENCE SCORE
# ============================================================

def calculate_confidence(
    pr,
    incident,
    review
):

    score = 0

    # Pull request approved
    if str(pr["Status"]).lower() == "approved":
        score += 40

    # Reviewer exists
    if str(review["Reviewer"]) != "Not Assigned":
        score += 20

    # Review approved
    if str(review["Decision"]).lower() == "approved":
        score += 30

    # Incident has verified resolution
    if str(
        incident["Final_Resolution"]
    ) != "Not verified yet":
        score += 10

    return score


# ============================================================
# GENERATE RUNBOOK
# ============================================================

def generate_runbook(pr_id):

    pr = get_pr(pr_id)

    incident = get_incident(pr_id)

    diff = get_diff(pr_id)

    review = get_review(pr_id)

    if pr is None:
        return None

    # Calculate confidence
    confidence = calculate_confidence(
        pr,
        incident,
        review
    )

    # Check high impact
    text = (
        str(pr["Title"])
        + " "
        + str(pr["Description"])
        + " "
        + str(pr["Resolution"])
    )

    high_impact_keywords = check_high_impact(text)

    runbook = {

        "PR_ID": pr_id,

        "Problem": incident["Problem"],

        "Root_Cause": incident["Discussion"],

        "Solution": pr["Resolution"],

        "Changed_File": diff["File"],

        "Old_Code": diff["Old_Code"],

        "New_Code": diff["New_Code"],

        "Verification": review["Comment"],

        "Reviewer": review["Reviewer"],

        "Review_Status": review["Decision"],

        "Confidence": confidence,

        "High_Impact": len(
            high_impact_keywords
        ) > 0,

        "Risk_Keywords": ", ".join(
            high_impact_keywords
        ),

        "Generated_At": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    return runbook


# ============================================================
# AUDIT LOG
# ============================================================

def add_audit(
    action,
    pr_id,
    details
):

    st.session_state.audit_log.append({

        "Time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "Action": action,

        "PR_ID": pr_id,

        "Details": details
    })


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🛠️ Maintenance Assistant"
)

st.sidebar.write(
    "Knowledge Capture System"
)

page = st.sidebar.radio(

    "Navigation",

    [
        "Dashboard",
        "Pull Requests",
        "Incidents",
        "Generate Runbook",
        "Review Runbooks",
        "Risk Checker",
        "Audit Trail",
        "Experiment"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title(
        "🛠️ Maintenance Knowledge Assistant"
    )

    st.write(
        "Convert completed software fixes "
        "into verified and reusable maintenance runbooks."
    )

    st.divider()

    # Metrics
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

        approved = len(
            reviews[
                reviews["Decision"] == "Approved"
            ]
        )

        st.metric(
            "Approved Reviews",
            approved
        )

    with col4:

        st.metric(
            "Runbooks Generated",
            len(
                st.session_state.runbooks
            )
        )

    st.divider()

    st.subheader(
        "📊 System Workflow"
    )

    st.info(
        """
        Completed Pull Request
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
        Reusable Maintenance Knowledge
        """
    )

    st.subheader(
        "🎯 Main Project Goal"
    )

    st.write(
        "Reduce the time required for a new engineer "
        "to repeat a previously solved maintenance fix."
    )

    st.success(
        "Synthetic and anonymised data is being used."
    )


# ============================================================
# PULL REQUESTS
# ============================================================

elif page == "Pull Requests":

    st.title(
        "📌 Pull Requests"
    )

    st.dataframe(
        pull_requests,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Pull Request Details"
    )

    pr_id = st.selectbox(
        "Select Pull Request",
        pull_requests["PR_ID"].tolist()
    )

    pr = get_pr(pr_id)

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

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Reviewer:**",
            pr["Reviewer"]
        )

    with col2:

        if pr["Status"] == "Approved":

            st.success(
                "Approved"
            )

        else:

            st.warning(
                "Pending"
            )


# ============================================================
# INCIDENTS
# ============================================================

elif page == "Incidents":

    st.title(
        "🚨 Incidents"
    )

    st.dataframe(
        incidents,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Incident Details"
    )

    pr_id = st.selectbox(
        "Select Incident",
        incidents["PR_ID"].tolist()
    )

    incident = get_incident(pr_id)

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

elif page == "Generate Runbook":

    st.title(
        "📖 Generate Maintenance Runbook"
    )

    st.write(
        "Select a Pull Request to convert "
        "the completed fix into reusable documentation."
    )

    pr_id = st.selectbox(

        "Select Pull Request",

        pull_requests["PR_ID"].tolist()
    )

    pr = get_pr(pr_id)

    review = get_review(pr_id)

    st.info(
        f"Reviewer decision: {review['Decision']}"
    )

    if st.button(
        "🚀 Generate Runbook",
        use_container_width=True
    ):

        runbook = generate_runbook(
            pr_id
        )

        st.session_state.runbooks.append(
            runbook
        )

        add_audit(

            "Runbook Generated",

            pr_id,

            "Runbook created using "
            "PR, incident, code diff and review."
        )

        st.success(
            "✅ Runbook generated successfully!"
        )

        st.divider()

        st.subheader(
            "📋 Generated Runbook"
        )

        st.write(
            "### 1. Problem"
        )

        st.write(
            runbook["Problem"]
        )

        st.write(
            "### 2. Root Cause / Evidence"
        )

        st.write(
            runbook["Root_Cause"]
        )

        st.write(
            "### 3. Solution"
        )

        st.success(
            runbook["Solution"]
        )

        st.write(
            "### 4. Changed File"
        )

        st.code(
            runbook["Changed_File"]
        )

        st.write(
            "### 5. Before"
        )

        st.code(
            runbook["Old_Code"]
        )

        st.write(
            "### 6. After"
        )

        st.code(
            runbook["New_Code"]
        )

        st.write(
            "### 7. Verification"
        )

        st.write(
            runbook["Verification"]
        )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Confidence",
                f"{runbook['Confidence']}%"
            )

        with col2:

            st.metric(
                "Review",
                runbook["Review_Status"]
            )

        with col3:

            if runbook["High_Impact"]:

                st.warning(
                    "⚠️ High Impact"
                )

            else:

                st.success(
                    "Normal Impact"
                )

        if runbook["High_Impact"]:

            st.warning(
                "Human confirmation is required "
                "because this fix contains a high-impact keyword."
            )

            st.write(
                "**Detected keyword(s):**",
                runbook["Risk_Keywords"]
            )


# ============================================================
# REVIEW RUNBOOKS
# ============================================================

elif page == "Review Runbooks":

    st.title(
        "👨‍💻 Human Review"
    )

    if len(
        st.session_state.runbooks
    ) == 0:

        st.info(
            "No runbooks have been generated yet."
        )

    else:

        for i, runbook in enumerate(
            st.session_state.runbooks
        ):

            with st.expander(
                f"Runbook {i + 1} - {runbook['PR_ID']}"
            ):

                st.write(
                    "**Problem:**",
                    runbook["Problem"]
                )

                st.write(
                    "**Solution:**",
                    runbook["Solution"]
                )

                st.write(
                    "**Confidence:**",
                    f"{runbook['Confidence']}%"
                )

                if runbook["High_Impact"]:

                    st.warning(
                        "⚠️ High-impact action detected. "
                        "Human confirmation is required."
                    )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✅ Approve",
                        key=f"approve_{i}"
                    ):

                        add_audit(

                            "Runbook Approved",

                            runbook["PR_ID"],

                            "Human reviewer approved runbook."
                        )

                        st.success(
                            "Runbook approved."
                        )

                with col2:

                    if st.button(
                        "❌ Reject",
                        key=f"reject_{i}"
                    ):

                        st.session_state[
                            f"reject_mode_{i}"
                        ] = True

                if st.session_state.get(
                    f"reject_mode_{i}",
                    False
                ):

                    reason = st.text_input(

                        "Reason for rejection",

                        key=f"reason_{i}"
                    )

                    if st.button(

                        "Submit Rejection",

                        key=f"submit_reject_{i}"
                    ):

                        if reason.strip() == "":

                            st.error(
                                "Please enter a rejection reason."
                            )

                        else:

                            add_audit(

                                "Runbook Rejected",

                                runbook["PR_ID"],

                                reason
                            )

                            st.warning(
                                "Runbook rejected and "
                                "reason recorded."
                            )


# ============================================================
# RISK CHECKER
# ============================================================

elif page == "Risk Checker":

    st.title(
        "⚠️ Risk Checker"
    )

    st.write(
        "This checks whether a maintenance fix "
        "contains keywords associated with high-impact actions."
    )

    pr_id = st.selectbox(

        "Select Pull Request",

        pull_requests["PR_ID"].tolist()
    )

    pr = get_pr(pr_id)

    text = (

        str(pr["Title"])

        + " "

        + str(pr["Description"])

        + " "

        + str(pr["Resolution"])
    )

    keywords = check_high_impact(
        text
    )

    if keywords:

        st.error(
            "⚠️ High-impact action detected."
        )

        st.write(
            "**Detected keyword(s):**"
        )

        st.write(
            ", ".join(keywords)
        )

        st.warning(
            "Human confirmation is required."
        )

    else:

        st.success(
            "✅ No high-impact keywords detected."
        )


# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "Audit Trail":

    st.title(
        "📝 Audit Trail"
    )

    st.write(
        "Every important action is recorded here."
    )

    if len(
        st.session_state.audit_log
    ) == 0:

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


# ============================================================
# EXPERIMENT / METRICS
# ============================================================

elif page == "Experiment":

    st.title(
        "🧪 Validation Experiment"
    )

    st.write(
        "Measure whether the assistant reduces "
        "the time required for a new engineer "
        "to repeat a known fix."
    )

    st.divider()

    baseline = st.number_input(

        "Baseline time without assistant (minutes)",

        min_value=1,

        value=30
    )

    assistant_time = st.number_input(

        "Time with assistant (minutes)",

        min_value=1,

        value=15
    )

    reduction = (

        (baseline - assistant_time)

        / baseline

    ) * 100

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Baseline",
            f"{baseline} min"
        )

    with col2:

        st.metric(
            "With Assistant",
            f"{assistant_time} min"
        )

    with col3:

        st.metric(
            "Time Reduction",
            f"{reduction:.1f}%"
        )

    st.divider()

    if reduction > 0:

        st.success(
            f"✅ The assistant reduced repeat-fix time "
            f"by {reduction:.1f}%."
        )

    elif reduction == 0:

        st.info(
            "The assistant produced no time reduction "
            "in this experiment."
        )

    else:

        st.warning(
            "The assistant took longer than the baseline."
        )

    st.subheader(
        "🎯 Main Metric"
    )

    st.write(
        "Reduction in time taken by a new engineer "
        "to repeat a known fix."
    )
