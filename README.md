

# Healthcare Record Validation Project

## Project Overview

This project simulates a healthcare data quality workflow for validating physician and clinic contact records. The goal is to identify missing, duplicated, or incorrectly formatted contact information before records are updated in internal systems or used for outreach.

This project mirrors common junior data analyst responsibilities in healthcare operations, including record maintenance, data validation, documentation, and follow-up tracking.

## Business Problem

Healthcare organizations often maintain physician and clinic records across multiple systems. Inaccurate contact information can slow down communication, reduce outreach response rates, and create inconsistent records across hospital or clinic systems.

This project answers the question:

> How can we validate physician and clinic contact records and create a repeatable process for identifying records that need correction or follow-up?

## Dataset

The sample dataset contains simulated physician and clinic records with fields such as:

- physician ID
- physician name
- clinic name
- specialty
- phone number
- email
- address
- last updated date
- outreach status

The raw dataset intentionally includes common data quality issues:

- missing phone numbers
- missing emails
- missing addresses
- invalid email formats
- invalid phone formats
- duplicated physician IDs
- records requiring outreach follow-up

## Data Quality Checks

The validation script checks for:

1. Missing required fields
2. Duplicate physician IDs
3. Invalid email formats
4. Invalid phone number formats
5. Records requiring outreach follow-up

## Tools Used

- Python
- pandas
- CSV files
- Data validation logic
- Documentation and reporting workflow


## Repository Structure

```text
healthcare-record-validation/
├── data/
│   └── physician_clinic_contacts_raw.csv
├── reports/
│   ├── physician_clinic_contacts_clean.csv
│   ├── record_validation_issues.csv
│   └── data_quality_summary.md
├── src/
│   └── validate_records.py
├── requirements.txt
└── README.md
```



## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the validation script:

```bash
python src/validate_records.py
```

The script creates:

- a cleaned contact record file
- a validation issues file
- a data quality summary report

## Key Outputs

### Cleaned Dataset

`reports/physician_clinic_contacts_clean.csv`

Includes normalized phone formatting and a `needs_follow_up` flag.

### Validation Issues

`reports/record_validation_issues.csv`

Lists each detected issue with:

- row number
- physician ID
- field name
- issue type
- original value

### Data Quality Summary

`reports/data_quality_summary.md`

Summarizes total records reviewed, issue counts, duplicate records, and follow-up needs.

## Example Findings

The validation process identifies:

- duplicate physician records
- records missing required contact fields
- invalid phone and email formats
- records requiring stakeholder follow-up

## Recommended Business Actions

1. Prioritize records marked as Pending or Needs Follow-up.
2. Contact clinics to confirm missing or invalid phone and email information.
3. Review duplicated physician IDs before updating production records.
4. Run validation checks on a recurring basis before publishing record updates.
5. Maintain documentation of assumptions and update logic for auditability.

## Resume Bullet Version

- Built a Python-based healthcare record validation workflow to identify missing fields, duplicate physician IDs, invalid phone/email formats, and outreach follow-up needs.
- Created cleaned datasets, issue logs, and data quality summary reports to support accurate physician and clinic record maintenance.
- Documented validation logic, assumptions, and recommended follow-up actions to improve data accuracy and operational transparency.
```