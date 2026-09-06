import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Maintenance Knowledge Assistant",
    page_icon="🛠️",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    pull_requests = pd.read_csv("data/pull_requests.csv")
    incidents = pd.read_csv("data/incidents.csv")
    code_diffs = pd.read_csv("data/code_diffs.csv")
    reviews = pd.read_csv("data/reviews.csv")

    return pull_requests, incidents, code_diffs, reviews


pull_requests, incidents, code_diffs, reviews = load_data()

# ============================================================
# SESSION STATE
# ============================================================

if "runbooks" not in st.session_state:
    st.session_state.runbooks = []

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []


# ============================================================
# FUNCTIONS
# ============================================================

def get_pr(pr_id):
    result = pull_requests[pull_requests["PR_ID"] == pr_id]

    if len(result) == 0:
        return None

    return result.iloc[0]


def get_incident(pr_id):
    result = incidents[incidents["PR_ID"] == pr_id]

    if len(result) == 0:
        return None

    return result.iloc[0]


def get_diff(pr_id):
    result = code_diffs[code_diffs["PR_ID"] == pr_id]

    if len(result) == 0:
        return None

    return result.iloc[0]


def get_review(pr_id):
    result = reviews[reviews["PR_ID"] == pr_id]

    if len(result) == 0:
        return None

    return result.iloc[0]


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

    for keyword in keywords:
        if keyword in text:
            return True

    return False


def calculate_confidence(pr, incident, review):

    score = 0

    # PR approved
    if str(pr["Status"]).lower() == "approved":
        score += 40

    # Reviewer available
    if str(review["Reviewer"]) != "Not Assigned":
        score += 20

    # Review approved
    if str(review["Decision"]).lower() == "approved":
        score += 30

    # Incident has resolution
    if str(incident["Final_Resolution"]) != "Not verified yet":
        score += 10

    return score


def generate_runbook(pr_id):

    pr = get_pr(pr_id)
    incident = get_incident(pr_id)
    diff = get_diff(pr_id)
    review = get_review(pr_id)

    if pr is None:
        return None

    confidence = calculate_confidence(
        pr,
        incident,
        review
    )

    high_impact = check_high_impact(
        str(pr["Title"]) +
        " " +
        str(pr["Description"])
    )

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
        "High_Impact": high_impact,
        "Generated_At": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    return runbook


def add_audit(action, pr_id, details):

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

st.sidebar.title("🛠️ Maintenance Assistant")

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

    st.title("🛠️ Maintenance Knowledge Assistant")

    st.write(
        "Convert completed software fixes into "
        "verified and reusable maintenance runbooks."
    )

    st.divider()

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
            len(st.session_state.runbooks)
        )

    st.divider()

    st.subheader("📊 Project Workflow")

    st.write("""
    1. Completed Pull Request
    ↓
    2. Incident Discussion
    ↓
    3. Code Diff
    ↓
    4. Reviewer Approval
    ↓
    5. Runbook Generation
    ↓
    6. Human Verification
    ↓
    7. Reusable Maintenance Knowledge
    """)

    st.success(
        "The system uses synthetic/anonymised data "
        "for demonstration."
    )


# ============================================================
# PULL REQUESTS
# ============================================================

elif page == "Pull Requests":

    st.title("📌 Pull Requests")

    st.dataframe(
        pull_requests,
        use_container_width=True
    )

    st.subheader("Pull Request Details")

    pr_id = st.selectbox(
        "Select Pull Request",
        pull_requests["PR_ID"].tolist()
    )

    pr = get_pr(pr_id)

    st.write("### Title")
    st.write(pr["Title"])

    st.write("### Description")
    st.write(pr["Description"])

    st.write("### Resolution")
    st.success(pr["Resolution"])

    st.write("### Reviewer")
    st.write(pr["Reviewer"])

    st.write("### Status")
    st.write(pr["Status"])


# ============================================================
# INCIDENTS
# ============================================================

elif page == "Incidents":

    st.title("🚨 Incidents")

    st.dataframe(
        incidents,
        use_container_width=True
    )

    st.subheader("Incident Details")

    pr_id = st.selectbox(
        "Select PR",
        incidents["PR_ID"].tolist()
    )

    incident = get_incident(pr_id)

    st.write("### Problem")
    st.write(incident["Problem"])

    st.write("### Team Discussion")
    st.write(incident["Discussion"])

    st.write("### Final Resolution")
    st.write(incident["Final_Resolution"])


# ============================================================
# GENERATE RUNBOOK
# ============================================================

elif page == "Generate Runbook":

    st.title("📖 Generate Maintenance Runbook")

    pr_id = st.selectbox(
        "Select completed Pull Request",
        pull_requests["PR_ID"].tolist()
    )

    pr = get_pr(pr_id)
    review = get_review(pr_id)

    st.info(
        f"Reviewer status: {review['Decision']}"
    )

    if st.button(
        "🚀 Generate Runbook",
        use_container_width=True
    ):

        runbook = generate_runbook(pr_id)

        st.session_state.runbooks.append(
            runbook
        )

        add_audit(
            "Runbook Generated",
            pr_id,
            "Runbook created from PR, incident, "
            "code diff and review."
        )

        st.success(
            "Runbook generated successfully!"
        )

        st.divider()

        st.subheader("📋 Maintenance Runbook")

        st.write("### Problem")
        st.write(runbook["Problem"])

        st.write("### Root Cause / Evidence")
        st.write(runbook["Root_Cause"])

        st.write("### Solution")
        st.success(runbook["Solution"])

        st.write("### Changed File")
        st.code(runbook["Changed_File"])

        st.write("### Before")
        st.code(runbook["Old_Code"])

        st.write("### After")
        st.code(runbook["New_Code"])

        st.write("### Verification")
        st.write(runbook["Verification"])

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
                st.warning("High Impact")
            else:
                st.success("Normal Impact")


# ============================================================
# REVIEW RUNBOOKS
# ============================================================

elif page == "Review Runbooks":

    st.title("👨‍💻 Human Review")

    if len(st.session_state.runbooks) == 0:

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

                        add_audit(
                            "Runbook Rejected",
                            runbook["PR_ID"],
                            reason
                        )

                        st.warning(
                            "Runbook rejected and reason recorded."
                        )


# ============================================================
# RISK CHECKER
# ============================================================

elif page == "Risk Checker":

    st.title("⚠️ Risk Checker")

    st.write(
        "This checks whether a fix contains "
        "keywords associated with high-impact changes."
    )

    pr_id = st.selectbox(
        "Select PR",
        pull_requests["PR_ID"].tolist()
    )

    pr = get_pr(pr_id)

    text = (
        str(pr["Title"]) +
        " " +
        str(pr["Description"]) +
        " " +
        str(pr["Resolution"])
    )

    if check_high_impact(text):

        st.error(
            "⚠️ High-impact action detected."
        )

        st.write(
            "Human confirmation is required before "
            "the action can be considered verified."
        )

    else:

        st.success(
            "✅ No high-impact keywords detected."
        )


# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "Audit Trail":

    st.title("📝 Audit Trail")

    if len(st.session_state.audit_log) == 0:

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
# EXPERIMENT
# ============================================================

elif page == "Experiment":

    st.title("🧪 Validation Experiment")

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
