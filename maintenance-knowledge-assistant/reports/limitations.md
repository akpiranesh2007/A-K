# Limitations Report

## 1. Prototype Scope

The Maintenance Knowledge-Capture Assistant is a working prototype designed to demonstrate how completed maintenance fixes can be converted into evidence-backed and reviewer-approved runbooks.

It is not intended to operate as an autonomous production maintenance system.

---

## 2. Synthetic and Anonymised Data

The prototype uses synthetic or anonymised data.

The validation dataset contains simulated:

- Pull requests
- Incident discussions
- Code diffs
- Reviewer resolutions
- Maintenance timings

No production credentials, secrets, customer information, or personally identifiable information are required.

---

## 3. Privacy Assumptions

The prototype assumes:

1. Production secrets are never stored in the validation dataset.
2. Personal information is removed or anonymised.
3. Confidential source code is not required for demonstration.
4. Synthetic identifiers are used for engineers, reviewers, incidents, and pull requests.
5. Access to maintenance information would require appropriate authentication and authorization in a production implementation.
6. Audit records should follow the organization's retention and access policies.
7. Sensitive incident information should not be exposed to unauthorized users.

---

## 4. Evidence Limitations

The assistant depends on the availability and quality of:

- Pull request information
- Incident discussions
- Code diffs
- Reviewer approvals

If one of these sources is missing, the assistant cannot provide the same level of verification.

The prototype therefore warns or blocks actions when required evidence is unavailable.

---

## 5. AI / Recommendation Limitations

The recommendation logic is rule-based in the prototype.

The confidence score is based on explicit evidence rules:

- Pull Request available: +40
- Incident discussion available: +15
- Code diff available: +15
- Reviewer approved: +30

The score is capped at 100%.

A high confidence score does not guarantee that a maintenance procedure is technically correct.

Human review remains necessary.

---

## 6. High-Impact Action Limitations

High-impact actions require human confirmation.

Examples include maintenance involving:

- Security
- Authentication
- Databases
- Production systems

The assistant does not independently execute these high-impact actions.

A reviewer must confirm the action and the decision is recorded in the audit trail.

---

## 7. Override Limitations

Reviewers can override assistant recommendations, but an override reason is required.

This prevents unexplained changes from being silently accepted.

The override reason is retained as part of the audit record.

---

## 8. Rollback Limitations

The prototype provides a rollback workflow and records rollback decisions.

However, the prototype does not directly modify production infrastructure.

The rollback workflow demonstrates:

- Change review
- Human confirmation
- Rollback reason
- Audit recording

A production implementation would need integration with the organization's actual deployment and version-control systems.

---

## 9. Validation Limitations

The current validation experiment uses 10 synthetic cases.

The measured result was:

- Baseline average: 20.7 minutes
- Assistant average: 11.3 minutes
- Average time saved: 9.3 minutes
- Measured reduction: 45.0%
- Target: 30.0%

The measured 45.0% reduction exceeds the prototype target.

However, this result must not be interpreted as a production performance guarantee because the dataset is synthetic and the sample size is small.

---

## 10. User Validation Limitations

The stakeholder validation was a short prototype review.

It does not represent a large-scale usability study.

Future validation should include multiple engineers and a larger number of maintenance tasks.

---

## 11. Generalisation Limitations

Maintenance problems vary significantly between systems.

A runbook that is correct for one service may not be correct for another service.

Therefore, runbooks should retain their supporting evidence and should be reviewed before reuse in a different environment.

---

## 12. Production Readiness Limitations

Before production deployment, the system would require additional work in:

- Authentication
- Authorization
- Secret management
- Secure API integration
- Production logging
- Data retention
- Access control
- Monitoring
- Reliability testing
- Security testing
- Larger-scale validation

---

## 13. Safe-Failure Principle

The prototype intentionally prefers a safe failure over an unsupported recommendation.

When important evidence is missing, the system should:

1. Identify the missing evidence.
2. Warn the reviewer.
3. Reduce verification confidence where appropriate.
4. Block approval when required.
5. Require human confirmation for high-impact actions.
6. Record important decisions in the audit trail.

---

## 14. Conclusion

The prototype demonstrates a controlled maintenance knowledge-capture workflow rather than an autonomous maintenance agent.

Its main limitations are the use of synthetic data, a small validation sample, rule-based confidence scoring, limited stakeholder testing, and the absence of direct production-system execution.

These limitations are explicitly documented so that the prototype's results are not overstated.
