# Maintenance Knowledge-Capture Assistant

## 1. Project Overview

The Maintenance Knowledge-Capture Assistant is a working prototype that converts completed software maintenance fixes into verified, reusable runbooks.

The problem addressed is knowledge loss when experienced engineers leave an organization and previously solved maintenance problems are not converted into reusable documentation.

The prototype combines:

- Pull requests
- Incident discussions
- Code diffs
- Reviewer-approved resolutions
- Evidence-based recommendations
- Human confirmation
- Override reasons
- Audit trails
- Change review
- Rollback controls
- Edge-case validation
- Measurable validation experiments

The prototype uses synthetic or anonymised data.

---

## 2. Problem Statement

In an open-source library used internally by multiple products, maintenance knowledge can become concentrated in individual engineers.

When an engineer leaves:

- Previous fixes may be difficult to discover.
- Incident knowledge may remain inside discussions.
- Code changes may not be converted into reusable procedures.
- New engineers may spend significant time rediscovering known fixes.

The goal is to capture completed maintenance knowledge and convert it into verified runbooks that can be reused by future engineers.

---

## 3. Objectives

The prototype aims to:

1. Capture knowledge from completed maintenance fixes.
2. Combine multiple evidence sources.
3. Generate reusable maintenance runbooks.
4. Explain the evidence behind recommendations.
5. Require human confirmation for high-impact actions.
6. Capture override and rejection reasons.
7. Maintain a complete audit trail.
8. Provide change review and rollback paths.
9. Validate edge and failure cases.
10. Measure reduction in time required to repeat known fixes.

---

## 4. Evidence Sources

The assistant uses four main evidence sources.

### Pull Requests

Provide information about:

- Fix title
- Problem description
- Resolution
- Changed files
- Reviewer information

### Incident Discussions

Provide information about:

- Original problem
- Root cause
- Incident resolution

### Code Diffs

Provide evidence of:

- Previous implementation
- Updated implementation
- Actual maintenance change

### Reviewer-Approved Resolutions

Provide human verification that the proposed resolution was reviewed and approved.

---

## 5. Evidence-Based Recommendation

The assistant displays the evidence supporting each recommendation.

The evidence panel includes:

- Pull Request Evidence
- Incident Evidence
- Code Diff Evidence
- Reviewer Evidence
- Evidence Completeness
- Explanation of why the recommendation was generated

The system does not silently present a recommendation without showing its supporting evidence.

---

## 6. Confidence Rules

The prototype uses explicit evidence rules.

| Evidence | Score |
|---|---:|
| Pull Request available | +40 |
| Incident discussion available | +15 |
| Code diff available | +15 |
| Reviewer approved | +30 |

Maximum confidence is capped at 100%.

Example:

```text
40 + 15 + 15 + 30 = 100%
