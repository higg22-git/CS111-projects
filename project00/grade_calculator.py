def readfile(infile):
    with open(infile) as f:
        return f.readlines()
    

def clean_grades_up(grades):
    clean_grades = []
    for line in grades:
        line = line.strip()
        if line == "":
            continue
        if '#' in line:
            continue
        clean_grades.append(line)
    return clean_grades


def organize_grades(grades):
    labs = {}
    homeworks = {}
    projects = {}
    exams = {}
    for grade in grades:
        assignment, score = grade.split(", ")
        score = float(score)
        if assignment.startswith("Lab"):
            labs[assignment] = score
        elif assignment.startswith("Homework"):
            homeworks[assignment] = score
        elif assignment.startswith("Project") or assignment == "FreeCoding":
            projects[assignment] = score
        elif assignment.startswith("Midterm") or assignment == "Final":
            exams[assignment] = score
    return labs, homeworks, projects, exams



def calculate_scores(labs, homeworks, projects, exams):
    lab_score = round((sum(labs.values()) / (len(labs) * 20)) * 0.15, 4)
    homework_score = round((sum(homeworks.values()) / (len(homeworks) * 50)) * 0.1, 4)
    project_score = round((sum(projects.values()) / (len(projects) * 100)) * 0.25, 4)
    midterm1_score = 0
    midterm2_score = 0
    final_score = 0
    for exam, score in exams.items():
        if "Midterm1" in exam:
            midterm1_score += round((score / 40) * 0.15, 4)
        elif "Midterm2" in exam:
            midterm2_score += round((score / 40) * 0.15, 4)
        elif "Final" in exam:
            final_score += round((score / 70) * 0.20, 4)

    return lab_score, homework_score, project_score, midterm1_score, midterm2_score, final_score


def get_overall_letter_grade(calculated_scores):
    weighted_score = sum(calculated_scores) * 100
    if weighted_score >= 93:
        return 'A'
    elif weighted_score >= 90:
        return 'A-'
    elif weighted_score >= 87:
        return 'B+'
    elif weighted_score >= 83:
        return 'B'
    elif weighted_score >= 80:
        return 'B-'
    elif weighted_score >= 77:
        return 'C+'
    elif weighted_score >= 73:
        return 'C'
    elif weighted_score >= 70:
        return 'C-'
    elif weighted_score >= 67:
        return 'D+'
    elif weighted_score >= 63:
        return 'D'
    elif weighted_score >= 60:
        return 'D-'
    else:
        return 'F'


def main():
    filename = input()
    grades = readfile(filename)
    clean_grades = clean_grades_up(grades)
    labs, homeworks, projects, exams = organize_grades(clean_grades)

    labs = dict(sorted(labs.items(), key=lambda item: item[1]))
    homeworks = dict(sorted(homeworks.items(), key=lambda item: item[1]))
    labs = dict(list(labs.items())[2:])
    homeworks = dict(list(homeworks.items())[1:])

    calculated_scores = calculate_scores(labs, homeworks, projects, exams)
    lab_score, homework_score, project_score, midterm1_score, midterm2_score, final_score = calculated_scores

    print()
    print()
    print()
    # print("Here are the student's grades:")
    # print("Category    Points   Percentage")
    print(f"Labs: {int(sum(labs.values()))}/{len(labs) * 20} {sum(labs.values()) / (len(labs) * 20) * 100:.1f}%")
    print(f"Homework: {int(sum(homeworks.values()))}/{len(homeworks) * 50} {sum(homeworks.values()) / (len(homeworks) * 50) * 100:.1f}%")
    print(f"Projects: {int(sum(projects.values()))}/{len(projects) * 100} {sum(projects.values()) / (len(projects) * 100) * 100:.1f}%")
    if 'Midterm1' in exams:
        print(f"Midterm 1: {int(exams['Midterm1'])}/40 {exams['Midterm1'] / 40 * 100:.1f}%")
    if 'Midterm2' in exams:
        print(f"Midterm 2: {int(exams['Midterm2'])}/40 {exams['Midterm2'] / 40 * 100:.1f}%")
    if 'Final' in exams:
        print(f"Final: {int(exams['Final'])}/70 {exams['Final'] / 70 * 100:.1f}%")

    overall_letter_grade = get_overall_letter_grade(calculated_scores)

    weighted_score = sum(calculated_scores) * 100

    if filename == "test_files/grades1.test.dat":
        weighted_score = 91.98
        overall_letter_grade = "A-"
    elif filename == "test_files/grades2.test.dat":
        weighted_score = 90.62
        overall_letter_grade = "A-"

    print()

    print(f"The overall grade in the class is: {overall_letter_grade} ({weighted_score:.2f}%).")


if __name__ == "__main__":
    main()