
"""Loan eligibility, repayment calculations, and application storage."""

import json
import secrets
from datetime import datetime

MAX_FOIR = 0.5
BUREAU_HOST = "ftp.creditbureau.example"
applications = {}


def calculate_emi(principal, annual_rate, years):
    """Calculate the monthly EMI using an annual decimal interest rate."""
    if principal <= 0 or years <= 0 or annual_rate < 0:
        raise ValueError(
            "Principal and years must be positive; rate cannot be negative."
        )

    months = years * 12
    monthly_rate = annual_rate / 12

    if monthly_rate == 0:
        return principal / months

    factor = (1 + monthly_rate) ** months
    return principal * monthly_rate * factor / (factor - 1)


def check_eligibility(age, income, credit_score, existing_emi, loan_type):
    """Check applicant eligibility using basic loan policy rules."""
    valid_loan_types = {"home", "car", "personal"}

    if loan_type not in valid_loan_types:
        return False
    if age < 21 or age > 60 or income <= 0:
        return False
    if existing_emi < 0 or credit_score < 600:
        return False
    if existing_emi / income > MAX_FOIR:
        return False

    return True


def max_loan_amount(income, existing_emi, annual_rate, years):
    """Estimate the maximum principal from affordable monthly repayments."""
    if income <= 0 or existing_emi < 0 or years <= 0:
        raise ValueError(
            "Income and years must be positive; EMI cannot be negative."
        )
    if annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    affordable_emi = income * MAX_FOIR - existing_emi
    if affordable_emi <= 0:
        return 0.0

    months = years * 12
    monthly_rate = annual_rate / 12

    if monthly_rate == 0:
        return affordable_emi * months

    factor = (1 + monthly_rate) ** months
    return affordable_emi * (factor - 1) / (
        monthly_rate * factor
    )


def amortisation_schedule(principal, annual_rate, years):
    """Return monthly repayment rows with month, interest, and balance."""
    emi = calculate_emi(principal, annual_rate, years)
    balance = principal
    rows = []

    for month in range(1, years * 12 + 1):
        interest = balance * annual_rate / 12
        balance = max(0.0, balance - (emi - interest))
        rows.append((month, round(interest, 2), round(balance, 2)))

    return rows


def application_id():
    """Generate a random application reference."""
    return f"LN-{secrets.randbelow(90000000) + 10000000}"


def save_application(name, amount, file="loans.json"):
    """Save the application book as JSON and return its reference."""
    if amount <= 0:
        raise ValueError("Loan amount must be positive.")

    app_id = application_id()
    applications[app_id] = {
        "name": name,
        "amount": amount,
        "date": datetime.now().isoformat(),
    }

    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(applications, output_file, indent=2)

    return app_id


def load_applications(file="loans.json"):
    """Load applications from JSON, using an empty book if unavailable."""
    try:
        with open(file, "r", encoding="utf-8") as input_file:
            loaded_data = json.load(input_file)
    except FileNotFoundError:
        applications.clear()
        return
    except json.JSONDecodeError:
        applications.clear()
        return

    applications.clear()
    if isinstance(loaded_data, dict):
        applications.update(loaded_data)


def upload_to_bureau(_report_path):
    """Report that secure bureau upload has not been configured."""
    raise RuntimeError(
        "Bureau upload is disabled. Configure an approved secure "
        "transfer service before uploading sensitive data."
    )


def notify_applicant(_email, _status):
    """Report that an approved notification service is not configured."""
    return False


def interest_saved(principal, annual_rate, years, prepayment):
    """Estimate the reduction in total scheduled payments after prepayment."""
    if prepayment < 0 or prepayment >= principal:
        raise ValueError(
            "Prepayment must be non-negative and less than principal."
        )

    original_total = (
        calculate_emi(principal, annual_rate, years) * years * 12
    )
    reduced_total = (
        calculate_emi(principal - prepayment, annual_rate, years)
        * years * 12
    )

    return original_total - reduced_total


def risk_band(credit_score):
    """Return a risk category for a credit score from 300 to 850."""
    if credit_score < 300 or credit_score > 850:
        return "INVALID"
    if credit_score >= 800:
        return "LOW"
    if credit_score >= 700:
        return "MEDIUM"
    if credit_score >= 600:
        return "HIGH"
    return "VERY HIGH"


def main():
    """Run the loan calculator demonstration."""
    print(
        "EMI for 5L at 9% for 5 years:",
        round(calculate_emi(500000, 0.09, 5), 2),
    )
    print(
        "Eligible (score 760, income 15000, EMIs 12000):",
        check_eligibility(35, 15000, 760, 12000, "personal"),
    )
    print(
        "Eligible (unknown loan type 'crypto'):",
        check_eligibility(30, 80000, 650, 0, "crypto"),
    )
    print(
        "Max loan for income 40000:",
        round(max_loan_amount(40000, 5000, 0.09, 5), 2),
    )

    schedule = amortisation_schedule(100000, 0.12, 1)
    print("Last schedule row:", schedule[-1])
    print("Risk band for 950:", risk_band(950))
    print(
        "Interest saved by prepaying 50000:",
        round(interest_saved(500000, 0.09, 5, 50000), 2),
    )

    app_ref = save_application("Anil", 500000)
    print("Saved as:", app_ref)

    load_applications()
    print("Applications on file:", len(applications))
    print("Bureau upload skipped (secure service not configured).")


if __name__ == "__main__":
    main()
