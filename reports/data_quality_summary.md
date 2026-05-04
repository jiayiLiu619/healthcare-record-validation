# Data Quality Summary

## Project Goal

Validate simulated physician and clinic contact records to support accurate record maintenance,
outreach tracking, and data quality monitoring.

## Summary Metrics

| Metric | Value |
|---|---:|
| Total records reviewed | 12 |
| Unique physician IDs | 11 |
| Total data quality issues found | 8 |
| Records needing outreach follow-up | 6 |
| Duplicate physician ID rows | 2 |

## Issue Breakdown

| Issue Type | Count |
|---|---:|
| missing_required_value | 4 |
| duplicate_physician_id | 2 |
| invalid_email_format | 1 |
| invalid_phone_format | 1 |


## Recommended Actions

1. Confirm missing phone, email, address, and last updated fields with the relevant clinic or physician office.
2. Review duplicate physician IDs and merge or remove duplicate records after confirmation.
3. Correct invalid email and phone formats before downstream reporting.
4. Prioritize records with Pending or Needs Follow-up outreach status.
5. Maintain a recurring validation process before updating production records.

## Outputs

- `reports/physician_clinic_contacts_clean.csv`
- `reports/record_validation_issues.csv`
- `reports/data_quality_summary.md`
