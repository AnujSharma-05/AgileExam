import sys

PASS_PERCENTAGE = 40


def calculate_result(marks, total):
    invalid = {"percentage": None, "grade": None, "status": "INVALID"}

    if isinstance(marks, bool) or isinstance(total, bool):
        return invalid
    if not isinstance(marks, (int, float)) or not isinstance(total, (int, float)):
        return invalid
    if total <= 0 or marks < 0 or marks > total:
        return invalid

    percentage = round(marks / total * 100, 2)

    if percentage >= 75:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= PASS_PERCENTAGE:
        grade = "C"
    else:
        grade = "F"

    status = "PASS" if percentage >= PASS_PERCENTAGE else "FAIL"
    return {"percentage": percentage, "grade": grade, "status": status}


def main():
    result = calculate_result(78, 100)
    print(f"Result: {result}")
    if result["status"] == "INVALID":
        sys.exit(1)


if __name__ == "__main__":
    main()
