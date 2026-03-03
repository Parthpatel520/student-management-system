def calculate_grade(marks_obtained, total_marks):
    percentage = (marks_obtained / total_marks) * 100

    if percentage >= 90:
        return "A"
    elif percentage >= 75:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "F"