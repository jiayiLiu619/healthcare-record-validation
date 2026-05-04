#!/usr/bin/env python3
"""
Healthcare Record Validation Project

Validates simulated physician and clinic contact records by checking:
- missing required fields
- duplicate physician IDs
- invalid phone numbers
- invalid email formats
- outreach follow-up needs

Run:
    python src/validate_records.py
"""

from pathlib import Path
import re
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "physician_clinic_contacts_raw.csv"

REPORTS_DIR = BASE_DIR / "reports"
CLEAN_FILE = REPORTS_DIR / "physician_clinic_contacts_clean.csv"
ISSUES_FILE = REPORTS_DIR / "record_validation_issues.csv"
SUMMARY_FILE = REPORTS_DIR / "data_quality_summary.md"

REQUIRED_FIELDS = [
    "physician_id",
    "physician_name",
    "clinic_name",
    "phone",
    "email",
    "address",
    "last_updated",
    "outreach_status",
]

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^\d{3}-\d{3}-\d{4}$")


def normalize_phone(value: str) -> str:
    """
    Convert 10-digit phone strings into XXX-XXX-XXXX format when possible.
    Example:
        4165550199 -> 416-555-0199
    """
    if pd.isna(value):
        return ""

    digits = re.sub(r"\D", "", str(value))

    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

    return str(value).strip()


def add_issue(
    issues: list,
    row_index: int,
    physician_id: str,
    field: str,
    issue_type: str,
    value: str,
) -> None:
    """
    Add a validation issue to the issue log.
    row_index + 2 is used because:
    - pandas index starts at 0
    - CSV row 1 is the header
    """
    issues.append(
        {
            "row_number": row_index + 2,
            "physician_id": physician_id,
            "field": field,
            "issue_type": issue_type,
            "value": value,
        }
    )


def main() -> None:
    REPORTS_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(INPUT_FILE, dtype=str).fillna("")
    issues = []

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    df["phone"] = df["phone"].apply(normalize_phone)

    for idx, row in df.iterrows():
        for field in REQUIRED_FIELDS:
            if row.get(field, "") == "":
                add_issue(
                    issues=issues,
                    row_index=idx,
                    physician_id=row.get("physician_id", ""),
                    field=field,
                    issue_type="missing_required_value",
                    value="",
                )

    duplicate_mask = df.duplicated(subset=["physician_id"], keep=False)

    for idx, row in df[duplicate_mask].iterrows():
        add_issue(
            issues=issues,
            row_index=idx,
            physician_id=row["physician_id"],
            field="physician_id",
            issue_type="duplicate_physician_id",
            value=row["physician_id"],
        )

    for idx, row in df.iterrows():
        email = row["email"]
        phone = row["phone"]

        if email and not EMAIL_PATTERN.match(email):
            add_issue(
                issues=issues,
                row_index=idx,
                physician_id=row["physician_id"],
                field="email",
                issue_type="invalid_email_format",
                value=email,
            )

        if phone and not PHONE_PATTERN.match(phone):
            add_issue(
                issues=issues,
                row_index=idx,
                physician_id=row["physician_id"],
                field="phone",
                issue_type="invalid_phone_format",
                value=phone,
            )

    df["needs_follow_up"] = df["outreach_status"].str.lower().isin(
        ["pending", "needs follow-up", "needs follow up"]
    )

    issue_df = pd.DataFrame(issues)

    df.to_csv(CLEAN_FILE, index=False)
    issue_df.to_csv(ISSUES_FILE, index=False)

    total_records = len(df)
    unique_physicians = df["physician_id"].nunique()
    total_issues = len(issue_df)
    records_needing_followup = int(df["needs_follow_up"].sum())
    duplicate_records = int(duplicate_mask.sum())

    if not issue_df.empty:
        issue_counts = issue_df["issue_type"].value_counts().to_dict()
    else:
        issue_counts = {}

    summary = f"""# Data Quality Summary

## Project Goal

Validate simulated physician and clinic contact records to support accurate record maintenance,
outreach tracking, and data quality monitoring.

## Summary Metrics

| Metric | Value |
|---|---:|
| Total records reviewed | {total_records} |
| Unique physician IDs | {unique_physicians} |
| Total data quality issues found | {total_issues} |
| Records needing outreach follow-up | {records_needing_followup} |
| Duplicate physician ID rows | {duplicate_records} |

## Issue Breakdown

"""

    if issue_counts:
        summary += "| Issue Type | Count |\n"
        summary += "|---|---:|\n"

        for issue_type, count in issue_counts.items():
            summary += f"| {issue_type} | {count} |\n"
    else:
        summary += "No issues found.\n"

    summary += """

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
"""

    SUMMARY_FILE.write_text(summary, encoding="utf-8")

    print("Validation complete.")
    print(f"Clean file: {CLEAN_FILE}")
    print(f"Issues file: {ISSUES_FILE}")
    print(f"Summary file: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()