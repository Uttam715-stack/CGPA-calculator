def get_grade_point(marks):
    if marks >= 90:
        return 10
    elif marks >= 80:
        return 9
    elif marks >= 70:
        return 8
    elif marks >= 60:
        return 7
    elif marks >= 50:
        return 6
    elif marks >= 40:
        return 5
    elif marks >= 30:
        return 4
    elif marks >= 20:
        return 3
    elif marks >= 10:
        return 2
    elif marks >= 0:
        return 1
    else:
        return 0

def get_classification(cgpa):
    if cgpa >= 9:
        return "Distinction"
    elif cgpa >= 7:
        return "First Class"
    elif cgpa >= 6:
        return "Second Class"
    elif cgpa >= 5:
        return "Pass"
    else:
        return "Fail"


# Fixed subjects and credits
subjects = {
    "Physics": 3,
    "C Programming": 4,
    "Innovation and Design Thinking": 1,
    "Kannada": 1,
    "Mathematics for CS": 4,
    "Computer Aided Engineering Drawing": 4,
    "Elective": 3
}

total_points = 0
total_credits = 0

print("\n--- Enter Marks (0 - 100 only) ---\n")

for subject, credit in subjects.items():
    while True:
        try:
            marks = float(input(f"Enter marks for {subject}: "))
            
            if 0 <= marks <= 100:
                break
            else:
                print("Marks must be between 0 and 100. Try again.")
        
        except ValueError:
            print("Invalid input. Please enter numeric value.")

    grade_point = get_grade_point(marks)
    print(f"{subject} → Grade Point: {grade_point}\n")

    total_points += grade_point * credit
    total_credits += credit


cgpa = total_points / total_credits

print("Total Credits:", total_credits)
print("Final CGPA:", round(cgpa, 2))
print("Result:", get_classification(cgpa))