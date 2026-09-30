import json
import os

DATA_FILE = "data/student_data.json"


def load_data():
    """Load saved student data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {"student": "", "subjects": [], "marks": {}, "study_plan": []}

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {"student": "", "subjects": [], "marks": {}, "study_plan": []}


def save_data(data):
    """Save the current data."""
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def get_number(prompt, minimum, maximum):
    """Keep asking until the user enters a valid number."""
    while True:
        try:
            number = int(input(prompt))
            if minimum <= number <= maximum:
                return number
            print("Please enter a number between", minimum, "and", maximum)
        except ValueError:
            print("Please enter a valid number.")


def calculate_total(numbers):
    total = 0
    for number in numbers:
        total = total + number
    return total


def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    return calculate_total(numbers) / len(numbers)


def find_hardest_subject(subjects):
    if len(subjects) == 0:
        return None

    hardest = subjects[0]
    for subject in subjects:
        if subject["difficulty"] > hardest["difficulty"]:
            hardest = subject
    return hardest


def get_grade(percentage):
    if percentage >= 90:
        return "A"
    elif percentage >= 75:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    elif percentage >= 40:
        return "E"
    else:
        return "F"


def reverse_list(items):
    result = []
    for i in range(len(items) - 1, -1, -1):
        result.append(items[i])
    return result


def remove_duplicates(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def create_study_plan(data):
    print("\n--- Create Study Plan ---")

    name = input("Enter student name: ").strip()
    if name == "":
        print("Name cannot be empty.")
        return

    number_of_subjects = get_number("How many subjects? (1-10): ", 1, 10)
    subjects = []

    for i in range(number_of_subjects):
        print("\nSubject", i + 1)
        subject_name = input("Enter subject name: ").strip()
        if subject_name == "":
            subject_name = "Subject " + str(i + 1)

        difficulty = get_number("Difficulty (1-5): ", 1, 5)
        hours = get_number("Study hours per week (1-40): ", 1, 40)

        subject = {
            "name": subject_name,
            "difficulty": difficulty,
            "hours": hours
        }
        subjects.append(subject)

    # Higher difficulty and fewer available study hours means higher priority.
    for subject in subjects:
        subject["priority"] = subject["difficulty"] * 2 + max(0, 6 - subject["hours"])

    # Simple sorting method: put the highest priority subject first.
    for i in range(len(subjects)):
        for j in range(i + 1, len(subjects)):
            if subjects[j]["priority"] > subjects[i]["priority"]:
                subjects[i], subjects[j] = subjects[j], subjects[i]

    data["student"] = name
    data["subjects"] = subjects
    data["study_plan"] = [subject["name"] for subject in subjects]

    print("\nStudy plan created for", name)
    print("--------------------------------")
    for i, subject in enumerate(subjects):
        print(i + 1, ".", subject["name"],
              "| Difficulty:", subject["difficulty"],
              "| Hours:", subject["hours"],
              "| Priority:", subject["priority"])


def enter_marks(data):
    print("\n--- Enter Marks ---")

    if len(data["subjects"]) == 0:
        print("Please create a study plan first.")
        return

    marks = {}
    for subject in data["subjects"]:
        mark = get_number("Marks for " + subject["name"] + " (0-100): ", 0, 100)
        marks[subject["name"]] = mark

    data["marks"] = marks
    print("Marks saved successfully.")


def show_performance(data):
    print("\n--- Performance Report ---")

    if len(data["marks"]) == 0:
        print("No marks have been entered yet.")
        return

    marks = list(data["marks"].values())
    total = calculate_total(marks)
    average = calculate_average(marks)

    print("Student:", data["student"])
    print("----------------------------")
    for subject, mark in data["marks"].items():
        print(subject, ":", mark)

    print("----------------------------")
    print("Total:", total)
    print("Average:", round(average, 2))
    print("Grade:", get_grade(average))


def show_analytics(data):
    print("\n--- Study Analytics ---")

    if len(data["subjects"]) == 0:
        print("No study plan found.")
        return

    hardest = find_hardest_subject(data["subjects"])
    print("Most difficult subject:", hardest["name"])

    if len(data["marks"]) > 0:
        lowest_subject = None
        lowest_mark = 101

        for subject, mark in data["marks"].items():
            if mark < lowest_mark:
                lowest_mark = mark
                lowest_subject = subject

        print("Lowest scoring subject:", lowest_subject)
        print("Lowest marks:", lowest_mark)

    print("\nPriority is calculated using:")
    print("difficulty x 2 + extra priority for fewer study hours")


def show_saved_data(data):
    print("\n--- Saved Data ---")
    if data["student"] == "":
        print("No student data saved yet.")
        return

    print("Student:", data["student"])
    print("Subjects:", len(data["subjects"]))
    print("Study order:", ", ".join(data["study_plan"]))


def main():
    data = load_data()

    while True:
        print("\n================================")
        print(" SMART STUDY PLANNER")
        print("================================")
        print("1. Create / Update Study Plan")
        print("2. Enter Subject Marks")
        print("3. Show Performance")
        print("4. Show Analytics")
        print("5. Show Saved Data")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_study_plan(data)
            save_data(data)
        elif choice == "2":
            enter_marks(data)
            save_data(data)
        elif choice == "3":
            show_performance(data)
        elif choice == "4":
            show_analytics(data)
        elif choice == "5":
            show_saved_data(data)
        elif choice == "6":
            print("Thank you for using Smart Study Planner!")
            break
        else:
            print("Invalid choice. Please select 1 to 6.")


if __name__ == "__main__":
    main()
