# Privacy & Data Protection

## 1. Data Used
This prototype uses synthetic and anonymised engineering data.

The dataset contains example:
- Pull requests
- Incident discussions
- Code changes
- Reviewer decisions
- Maintenance resolutions

No real customer information or confidential production data is used.

## 2. Privacy Assumptions
The production version should assume that engineering data may contain sensitive information.

Therefore:
- Personal information should be removed.
- Secrets and passwords must never be stored.
- API keys must never be included in runbooks.
- Customer information should be anonymised.
- Production credentials must not be sent to the assistant.
- Access should be restricted to authorised engineers.

## 3. Data Minimisation
The assistant should capture only information required to understand and reproduce a completed fix.

## 4. Human Review
Generated runbooks must be reviewed before becoming trusted maintenance knowledge.

High-impact actions require explicit human confirmation.

## 5. Audit Trail
Important actions should be recorded, including:
- Runbook generation
- Approval
- Rejection
- API data reception
- Rollback actions

## 6. Prototype Limitation
This prototype uses synthetic data and does not connect to a real production engineering system.
