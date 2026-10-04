# Error Analysis

## 1. Purpose

This report analyses the failure and edge cases observed during validation of the Maintenance Knowledge-Capture Assistant.

The assistant is designed to convert completed maintenance fixes into verified runbooks using:

- Pull request evidence
- Incident discussions
- Code diffs
- Reviewer-approved resolutions
- Human confirmation for high-impact actions
- Audit and rollback controls

The validation data is synthetic/anonymised.

---

## 2. Validation Summary

The validation dataset contains 10 synthetic maintenance cases.

| Metric | Result |
|---|---:|
| Total cases | 10 |
| Approved cases | 9 |
| Normal cases | 7 |
| Edge/failure cases | 3 |
| Baseline average | 20.7 minutes |
| Assistant average | 11.3 minutes |
| Average time saved | 9.3 minutes |
| Measured reduction | 45.0% |
| Target reduction | 30.0% |

The measured reduction of 45.0% is greater than the target of 30.0%.

---

## 3. Error and Failure Cases

### Case 1 — Missing Incident

**Condition**

The pull request contains a completed fix, but the corresponding incident discussion is unavailable.

**Expected behaviour**

The assistant must not claim that the root cause has been fully verified.

**System response**

The system displays a warning and marks root-cause evidence as incomplete.

**Impact**

The generated runbook has weaker evidence for explaining why the problem occurred.

**Mitigation**

A human reviewer should verify the root cause before treating the runbook as fully verified.

---

### Case 2 — Missing Code Diff

**Condition**

A pull request and incident may be available, but no usable code-diff evidence is available.

**Expected behaviour**

The assistant must not claim that the implementation change has been confirmed.

**System response**

The runbook is marked incomplete.

**Impact**

The system cannot independently verify exactly what implementation change fixed the issue.

**Mitigation**

Require the reviewer to provide or verify the relevant code change before approving the runbook.

---

### Case 3 — Pending Reviewer

**Condition**

The fix exists, but the reviewer has not approved the resolution.

**Expected behaviour**

The assistant must not allow the runbook to be treated as reviewer-verified.

**System response**

Runbook approval is blocked until reviewer approval is available.

**Impact**

The runbook cannot become a verified maintenance procedure.

**Mitigation**

Require reviewer approval before the runbook enters the verified state.

---

### Case 4 — High-Impact Change

**Condition**

The maintenance change contains indicators such as authentication, security, database, or production-related operations.

**Expected behaviour**

The assistant must not rely only on automated recommendation.

**System response**

Human confirmation is required before the high-impact action can proceed.

**Impact**

Additional human review is required, increasing the time needed for high-risk changes.

**Mitigation**

Keep human-in-the-loop confirmation mandatory and record the confirmation in the audit trail.

---

### Case 5 — Rollback Without Reason

**Condition**

A rollback is attempted without documenting why the rollback is required.

**Expected behaviour**

The rollback must not be recorded as a valid completed rollback.

**System response**

Rollback recording is blocked because a reason is required.

**Impact**

Prevents unexplained high-impact changes from being recorded without accountability.

**Mitigation**

Require a rollback reason and preserve the reason in the audit trail.

---

## 4. Error Analysis Table

| Failure Case | Risk | System Response | Human Action |
|---|---|---|---|
| Missing Incident | Incomplete root-cause evidence | Warning | Verify root cause |
| Missing Code Diff | Implementation cannot be verified | Mark incomplete | Verify code change |
| Pending Reviewer | Fix is not reviewer-approved | Block approval | Obtain reviewer approval |
| High-Impact Change | Potential operational impact | Require confirmation | Human confirmation |
| Rollback Without Reason | Poor accountability | Block rollback recording | Provide reason |

---

## 5. Why These Failures Are Important

The assistant is intentionally designed to fail safely when important evidence is unavailable.

Instead of generating a confident but unsupported runbook, it:

1. Detects missing evidence.
2. Explains what evidence is missing.
3. Reduces or blocks verification.
4. Requests human review when necessary.
5. Records important human decisions.
6. Prevents unexplained rollback actions.

This behaviour is preferable to silently generating an incorrect maintenance procedure.

---

## 6. Experiment Error Analysis

The validation experiment used synthetic baseline and assistant-assisted repeat-fix times.

The measured averages were:

- Baseline: 20.7 minutes
- Assistant-assisted: 11.3 minutes
- Average time saved: 9.3 minutes
- Measured reduction: 45.0%

The result exceeded the 30% target.

However, the result should not be interpreted as production performance because the experiment uses synthetic/anonymised validation data.

---

## 7. Sources of Experimental Error

### Synthetic Data

The validation dataset was created for prototype evaluation rather than collected from production systems.

Therefore, the measured 45.0% reduction may not represent the exact improvement achieved by real engineers.

### Small Sample Size

Only 10 validation cases were used.

A larger dataset would provide stronger evidence.

### Fixed Time Estimates

Baseline and assistant times in the validation dataset are predefined synthetic measurements.

They should eventually be replaced with measured timings from real or controlled user studies using anonymised tasks.

### Learning Effect

If the same engineer performs similar maintenance tasks multiple times, familiarity with the task may reduce completion time.

A controlled experiment should account for this effect.

### Task Difficulty

Different maintenance fixes may have different levels of complexity.

A more rigorous experiment should group cases by difficulty before comparing times.

---

## 8. Interpretation

The prototype demonstrates that verified maintenance knowledge can potentially reduce the time required for a new engineer to repeat a known fix.

The synthetic experiment achieved:

**45.0% measured reduction**

against a:

**30.0% target**

Therefore:

**Target achieved in the prototype validation.**

This result should be treated as prototype evidence rather than a production claim.

---

## 9. Recommended Future Validation

Future testing should:

1. Use a larger validation dataset.
2. Recruit new engineers or representative users.
3. Measure real task completion times.
4. Compare engineers with and without generated runbooks.
5. Record errors made during the task.
6. Separate low-risk and high-risk maintenance tasks.
7. Measure runbook correctness in addition to time reduction.
8. Continue using anonymised or synthetic data where required.

---

## 10. Conclusion

The assistant demonstrates safe failure behaviour when required maintenance evidence is incomplete.

The prototype does not blindly generate verified runbooks. It uses evidence checks, reviewer approval, human confirmation, audit logging, and rollback controls to reduce the risk of unsupported maintenance recommendations.

The current synthetic validation achieved a 45.0% reduction in repeat-fix time compared with the 30.0% target.

Further real-user validation is required before making production-level effectiveness claims.
