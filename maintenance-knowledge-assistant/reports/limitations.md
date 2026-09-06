# Prototype Limitations

## 1. Synthetic Dataset
The prototype uses synthetic/anonymised data.

## 2. Mock API
The API integration is simulated.

## 3. Rule-Based Risk Detection
The current risk checker uses keyword-based rules.

## 4. Prototype Rollback
The rollback manager only records and demonstrates a rollback path. It does not modify production code.

## 5. Runbook Generation
The current runbook generator uses structured data and rules. It is not a full large-language-model system.

## 6. Session Storage
Some prototype information is stored in Streamlit session state, so it is not yet a permanent enterprise knowledge database.

## 7. Validation Size
The experiment dataset is small. A production evaluation should use more maintenance tasks and engineers.

## 8. Human Validation
Generated knowledge still requires human review. The assistant should support engineers rather than independently making high-impact production decisions.

## 9. Future Improvements
- Real repository integration
- Real incident-management integration
- LLM-based runbook generation
- Vector database for knowledge retrieval
- Better risk classification
- Permanent database storage
- Authentication and role-based access
- Automated verification
- More extensive experiments
