import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Maintenance Knowledge Assistant",
    page_icon="🔧",
    layout="wide"
)

# ============================================================
# SYNTHETIC DATA
# ============================================================

pull_requests = pd.DataFrame([
    {
        "PR_ID": "PR101",
        "Title": "Fix Redis API timeout",
        "Description": "API requests were timing out because Redis timeout was too low.",
        "Resolution": "Increased Redis connection timeout from 5 to 30 seconds.",
        "Reviewer": "Reviewer001",
        "Status": "Approved"
    },
    {
        "PR_ID": "PR102",
        "Title": "Fix CSV parser crash",
        "Description": "CSV parser crashes when an empty row is present.",
        "Resolution": "Added validation to ignore empty rows.",
        "Reviewer": "Reviewer002",
        "Status": "Approved"
    },
    {
        "PR_ID": "PR103",
        "Title": "Fix memory issue",
        "Description": "Application memory increased during large file processing.",
        "Resolution": "Released unused object references after processing.",
        "Reviewer": "Reviewer003",
        "Status": "Approved"
    },
    {
        "PR_ID": "PR104",
        "Title": "Fix authentication issue",
        "Description": "Authentication fails for expired sessions.",
        "Resolution": "Added session expiration validation.",
        "Reviewer": "Not Assigned",
        "Status": "Pending"
    }
])

incidents = {
    "PR101": {
        "Incident": "INC001",
        "Problem": "API requests timeout during heavy usage.",
        "Discussion": "Team identified Redis connection timeout as the cause.",
        "Resolution": "Increase Redis timeout."
    },
    "PR102": {
        "Incident": "INC002",
        "Problem": "CSV parser crashes on empty rows.",
        "Discussion": "Empty rows were causing an exception.",
        "Resolution": "Validate rows before processing."
    },
    "PR103": {
        "Incident": "INC003",
        "Problem": "Memory usage increases during file processing.",
        "Discussion": "Unused objects remained in memory.",
        "Resolution": "Release unused references."
    },
    "PR104": {
        "Incident": "INC004",
        "Problem": "Users cannot authenticate after session expiry.",
        "Discussion": "Session expiration handling needs investigation.",
        "Resolution": "Not verified yet."
    }
}

code_diffs = {
    "PR101": {
        "File": "cache.py",
        "Old": "timeout = 5",
        "New": "timeout = 30"
    },
    "PR102": {
        "File": "parser.py",
        "Old": "process(row)",
        "New": "if row: process(row)"
    },
    "PR103": {
        "File": "memory.py",
        "Old": "objects kept in memory",
        "New": "objects released after processing"
    },
    "PR104": {
        "File": "auth.py",
        "Old": "authenticate(user)",
        "New": "authenticate(user, validate_session=True)"
    }
}

# ============================================================
# SESSION STATE
# ============================================================

if "runbooks" not in st.session_state:
    st.session_state.runbooks = []

if "audit" not in st.session_state:
    st.session_state.audit = []

# ============================================================
# FUNCTIONS
# ============================================================

def add_audit(action, details):
    st.session_state.audit.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Action": action,
        "Details": details
    })


def generate_runbook(pr):
    pr_id = pr["PR_ID"]

    incident = incidents[pr_id]
    diff = code_diffs[pr_id]

    # -----------------------------
    # Evidence rules
    # -----------------------------

    evidence = []

    evidence.append(f"Pull Request: {pr_id}")

    if incident:
        evidence.append(
            f"Incident: {incident['Incident']}"
        )

    if diff:
        evidence.append(
            f"Code Diff: {diff['File']}"
        )

    if pr["Status"] == "Approved":
        evidence.append(
            f"Reviewer approval by {pr['Reviewer']}"
        )

    # -----------------------------
    # Confidence calculation
    # -----------------------------

    confidence = 0

    if pr["Description"]:
        confidence += 20

    if pr["Resolution"]:
        confidence += 25

    if incident:
        confidence += 20

    if diff:
        confidence += 20

    if pr["Status"] == "Approved":
        confidence += 15

    verified = pr["Status"] == "Approved"

    # -----------------------------
    # Runbook
    # -----------------------------

    runbook = {
        "ID": f"RB-{pr_id}",
        "PR_ID": pr_id,
        "Title": pr["Title"],
        "Problem": incident["Problem"],
        "Root Cause": incident["Discussion"],
        "Solution": pr["Resolution"],
        "File Changed": diff["File"],
        "Old Code": diff["Old"],
        "New Code": diff["New"],
        "Verification": (
            "Reviewer approved the fix."
            if verified
            else
            "Reviewer approval is missing."
        ),
        "Confidence": confidence,
        "Status": "Verified" if verified else "Pending Review",
        "Evidence": evidence
    }

    return runbook


def is_high_impact(action):
    keywords = [
        "delete",
        "production database",
        "disable authentication",
        "drop database",
        "remove user data"
    ]

    action_lower = action.lower()

    return any(word in action_lower for word in keywords)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔧 Maintenance Assistant")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Pull Requests",
        "Generate Runbook",
        "Review Runbooks",
        "Audit Trail",
        "Risk Checker",
        "Experiment"
    ]
)

# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title("🔧 Maintenance Knowledge-Capture Assistant")

    st.write(
        "Convert completed software fixes into verified reusable runbooks."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Completed Fixes",
        len(pull_requests)
    )

    approved = len(
        pull_requests[
            pull_requests["Status"] == "Approved"
        ]
    )

    col2.metric(
        "Approved Fixes",
        approved
    )

    col3.metric(
        "Runbooks",
        len(st.session_state.runbooks)
    )

    col4.metric(
        "Pending Review",
        len([
            r for r in st.session_state.runbooks
            if r["Status"] == "Pending Review"
        ])
    )

    st.divider()

    st.subheader("System Workflow")

    st.write("""
    Completed Fix
    ↓
    Pull Request + Incident + Code Diff
    ↓
    Evidence Analysis
    ↓
    Runbook Generation
    ↓
    Human Review
    ↓
    Verified Runbook
    """)

# ============================================================
# PULL REQUESTS
# ============================================================

elif page == "Pull Requests":

    st.title("📋 Pull Requests")

    st.dataframe(
        pull_requests,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Select a Pull Request")

    pr_id = st.selectbox(
        "PR",
        pull_requests["PR_ID"]
    )

    pr = pull_requests[
        pull_requests["PR_ID"] == pr_id
    ].iloc[0]

    st.write("### Pull Request Details")

    st.write("**Title:**", pr["Title"])
    st.write("**Description:**", pr["Description"])
    st.write("**Resolution:**", pr["Resolution"])
    st.write("**Reviewer:**", pr["Reviewer"])
    st.write("**Status:**", pr["Status"])

    st.write("### Code Diff")

    diff = code_diffs[pr_id]

    col1, col2 = st.columns(2)

    with col1:
        st.error("Old Code")
        st.code(diff["Old"])

    with col2:
        st.success("New Code")
        st.code(diff["New"])

    st.write("### Incident Discussion")

    incident = incidents[pr_id]

    st.info(
        f"""
        Incident: {incident['Incident']}

        Problem: {incident['Problem']}

        Discussion: {incident['Discussion']}

        Resolution: {incident['Resolution']}
        """
    )

# ============================================================
# GENERATE RUNBOOK
# ============================================================

elif page == "Generate Runbook":

    st.title("📝 Generate Runbook")

    pr_id = st.selectbox(
        "Select completed fix",
        pull_requests["PR_ID"]
    )

    pr = pull_requests[
        pull_requests["PR_ID"] == pr_id
    ].iloc[0]

    st.write(
        f"Selected: **{pr['Title']}**"
    )

    if st.button(
        "🚀 Generate Runbook",
        type="primary"
    ):

        runbook = generate_runbook(pr)

        st.session_state.runbooks.append(
            runbook
        )

        add_audit(
            "Runbook Generated",
            f"{runbook['ID']} generated from {pr_id}"
        )

        st.success(
            f"Runbook {runbook['ID']} generated!"
        )

        st.subheader("Generated Runbook")

        st.write(
            f"### {runbook['Title']}"
        )

        st.write(
            "**Problem:**",
            runbook["Problem"]
        )

        st.write(
            "**Root Cause:**",
            runbook["Root Cause"]
        )

        st.write(
            "**Solution:**",
            runbook["Solution"]
        )

        st.write(
            "**File Changed:**",
            runbook["File Changed"]
        )

        st.write("### Code Change")

        col1, col2 = st.columns(2)

        with col1:
            st.error("Before")
            st.code(runbook["Old Code"])

        with col2:
            st.success("After")
            st.code(runbook["New Code"])

        st.write(
            "**Verification:**",
            runbook["Verification"]
        )

        st.write(
            f"**Confidence:** {runbook['Confidence']}%"
        )

        st.write(
            f"**Status:** {runbook['Status']}"
        )

        st.subheader("🔎 Evidence")

        for item in runbook["Evidence"]:
            st.write("✅", item)

# ============================================================
# REVIEW
# ============================================================

elif page == "Review Runbooks":

    st.title("👨‍💻 Human Review")

    if not st.session_state.runbooks:

        st.warning(
            "No runbooks available. Generate a runbook first."
        )

    else:

        for i, runbook in enumerate(
            st.session_state.runbooks
        ):

            st.divider()

            st.subheader(
                f"{runbook['ID']} - {runbook['Title']}"
            )

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

            st.write(
                "**Current Status:**",
                runbook["Status"]
            )

            if runbook["Status"] == "Pending Review":

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✅ Approve",
                        key=f"approve_{i}"
                    ):

                        runbook["Status"] = "Verified"

                        add_audit(
                            "Runbook Approved",
                            runbook["ID"]
                        )

                        st.success(
                            "Runbook approved."
                        )

                        st.rerun()

                with col2:

                    if st.button(
                        "❌ Reject",
                        key=f"reject_{i}"
                    ):

                        reason = st.text_input(
                            "Override / rejection reason",
                            key=f"reason_{i}"
                        )

                        if reason:

                            runbook["Status"] = "Rejected"

                            add_audit(
                                "Runbook Rejected",
                                f"{runbook['ID']} - {reason}"
                            )

                            st.error(
                                "Runbook rejected."
                            )

                            st.rerun()

# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "Audit Trail":

    st.title("📜 Complete Audit Trail")

    if st.session_state.audit:

        audit_df = pd.DataFrame(
            st.session_state.audit
        )

        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No audit events yet."
        )

# ============================================================
# RISK CHECKER
# ============================================================

elif page == "Risk Checker":

    st.title("⚠️ High-Impact Action Checker")

    st.write(
        "High-impact actions require human confirmation."
    )

    action = st.text_area(
        "Enter recommended action",
        placeholder="Example: Delete production database"
    )

    if st.button("Check Risk"):

        if not action:

            st.warning(
                "Please enter an action."
            )

        elif is_high_impact(action):

            st.error(
                "🔴 HIGH IMPACT ACTION"
            )

            st.warning(
                "Human confirmation is required before this action can proceed."
            )

            st.write(
                "**Action:**",
                action
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Approve Action"):
                    add_audit(
                        "High-Impact Action Approved",
                        action
                    )
                    st.success(
                        "Human approval recorded."
                    )

            with col2:
                if st.button("Reject Action"):
                    reason = st.text_input(
                        "Reason for rejection"
                    )

                    if reason:
                        add_audit(
                            "High-Impact Action Rejected",
                            f"{action} | Reason: {reason}"
                        )

                        st.error(
                            "Action rejected and reason recorded."
                        )

        else:

            st.success(
                "🟢 Low-impact action. Normal review process applies."
            )

# ============================================================
# EXPERIMENT
# ============================================================

elif page == "Experiment":

    st.title("📊 Validation Experiment")

    st.write(
        "Measure how much time a new engineer needs to repeat a known fix."
    )

    col1, col2 = st.columns(2)

    with col1:

        baseline = st.number_input(
            "Time without assistant (minutes)",
            min_value=1,
            value=120
        )

    with col2:

        with_assistant = st.number_input(
            "Time with assistant (minutes)",
            min_value=1,
            value=40
        )

    if st.button("Calculate Improvement"):

        reduction = (
            (baseline - with_assistant)
            / baseline
        ) * 100

        st.metric(
            "Time Reduction",
            f"{reduction:.1f}%"
        )

        result = pd.DataFrame({
            "Method": [
                "Without Assistant",
                "With Assistant"
            ],
            "Time (minutes)": [
                baseline,
                with_assistant
            ]
        })

        st.bar_chart(
            result.set_index("Method")
        )

        st.success(
            f"""
            Baseline: {baseline} minutes

            With Assistant: {with_assistant} minutes

            Improvement: {reduction:.1f}% reduction in maintenance time.
            """
        )

# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "Prototype uses synthetic/anonymised data only."
)