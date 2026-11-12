
def format_course_code(code):
    """
    Formats 'cs 301' as 'CS301'.
    Handles invalid and unexpected inputs safely.
    """
    if not isinstance(code, str):
        return ""

    parts = code.split()

    if len(parts) != 2:
        return ""

    dept, number = parts
    return dept.upper() + number


def total_credits(text):
    """
    Adds valid comma-separated whole-number credits.
    Invalid values are safely ignored.
    """
    if not isinstance(text, str):
        return 0

    total = 0

    for credit in text.split(','):
        try:
            value = int(credit.strip())

            if value >= 0:
                total += value

        except ValueError:
            continue

    return total


def parse_student_record(line):
    """
    Parses 'SRN|name|status' into a dictionary.
    Missing or invalid fields are handled safely.
    """
    if not isinstance(line, str):
        line = ""

    parts = line.split('|')

    srn = parts[0].strip().upper() if len(parts) > 0 else ""
    name = parts[1].strip() if len(parts) > 1 else ""
    status = parts[2].strip().lower() if len(parts) > 2 else ""

    return {
        "srn": srn,
        "name": name,
        "status": status
    }


def main():
    print("==== Running format_course_code ====")
    value = input("Enter a course code as DEPT NUMBER (e.g. cs 301): ")
    print("Formatted course code:", format_course_code(value))

    print("\n==== Running total_credits ====")
    value = input("Enter course credits separated by commas (e.g. 4,3,4): ")
    print("Total credits:", total_credits(value))

    print("\n==== Running parse_student_record ====")
    value = input("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ")
    print("Student record:", parse_student_record(value))


if __name__ == "__main__":
    main()
