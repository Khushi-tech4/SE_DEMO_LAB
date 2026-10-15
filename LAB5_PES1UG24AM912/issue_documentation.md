# Lab 5 — Static Code Analysis

## Objective
To improve the quality, security, and formatting of loan_calculator.py using Pylint, Bandit, and Flake8.

## Tools Used
- Pylint: checks code quality, naming, documentation, and programming practices.
- Bandit: identifies common Python security risks.
- Flake8: checks Python style and formatting.

## Issues Identified and Fixes

| Tool | Issues found before | Fixes applied |
|---|---|---|
| Pylint | Missing docstrings, inconsistent naming, mutable default arguments, built-in name shadowing, and file-handling issues | Added docstrings, used snake_case, removed the mutable default, renamed variables, and used context managers |
| Bandit | Unsafe serialization, non-cryptographic random identifiers, hardcoded credentials, and risky network/subprocess operations | Replaced marshal with JSON, used secrets for identifiers, removed hardcoded credentials, and disabled unconfigured transfer and notification operations |
| Flake8 | Unused imports, blank-line violations, long lines, and formatting issues | Removed unused imports and corrected spacing and formatting |

## Before-and-After Results

| Tool | Before | After |
|---|---|---|
| Pylint | 5.17/10 | 10.00/10 |
| Bandit | 8 findings | No issues identified |
| Flake8 | 21 violations | No reported violations |

## Functional Improvements
- Corrected EMI calculation to use an annual interest rate expressed as a decimal.
- Added input validation to loan calculations.
- Rejected unsupported loan types.
- Validated credit-score ranges in risk classification.
- Replaced marshal-based application storage with JSON.
- Used context managers for file operations.
- Disabled unconfigured bureau-upload and applicant-notification functionality.

## Conclusion
The final code achieved a Pylint score of 10.00/10, no Bandit findings, and no Flake8 violations. The program also executed successfully during functional testing.
