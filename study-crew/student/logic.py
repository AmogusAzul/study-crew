from django.db.models.query import QuerySet

from student.models import Student, Subject

import pandas as pd

def search_matches_by_subjects(student : Student, use_subjects : bool = False, subject_codes : set = set()) -> pd.DataFrame:

    if not use_subjects:
        
        subject_codes = get_subjects(student)

    df = pd.DataFrame(["student_id", "fairness", "sum", "count", "best", "worst", "squared_sum"])

    # Exclude blocked students and those who blocked the current student
    excluded_students = (student.user.contact.blocked_students.all() | student.user.contact.contacts.all()).select_related('student')

    subjects = Subject.objects.all().filter(
        subject_code__in=subject_codes
    ).exclude(
            student=student
    ).exclude(
        student__in=excluded_students
    )

    for entry in subjects:

        student_id = entry.student.id
        subject_code = entry.subject_code
        subject_delta = (get_students_subject(student, subject_code).score - entry.score)

        if df[df["student_id"] == student_id].empty:

            df = df.append({
                "student_id": student_id,
                "fairness": subject_delta,
                "sum": abs(subject_delta),
                "count": 1,
                "best": entry.score,
                "worst": entry.score,
                "squared_sum": subject_delta ** 2
            }, ignore_index=True)
        else:

            curr_fairness = df[df["student_id"] == student_id]["fairness"].values[0]
            curr_sum = df[df["student_id"] == student_id]["sum"].values[0]
            curr_count = df[df["student_id"] == student_id]["count"].values[0]
            curr_best = df[df["student_id"] == student_id]["best"].values[0]
            curr_worst = df[df["student_id"] == student_id]["worst"].values[0]
            curr_squared_sum = df[df["student_id"] == student_id]["squared_sum"].values[0]

            df.loc[df["student_id"] == student_id, "fairness"] = curr_fairness + subject_delta
            df.loc[df["student_id"] == student_id, "sum"] = curr_sum + abs(subject_delta)
            df.loc[df["student_id"] == student_id, "count"] = curr_count + 1
            df.loc[df["student_id"] == student_id, "squared_sum"] = curr_squared_sum + (subject_delta ** 2)

            if entry.score > curr_best:
                df.loc[df["student_id"] == student_id, "best"] = entry.score

            if entry.score < curr_worst:
                df.loc[df["student_id"] == student_id, "worst"] = entry.score

    # Calculate abs of the fairness
    df["fairness"] = df["fairness"].apply(lambda x: abs(x))

    df["avg"] = df["sum"] / df["count"]

    df["std"] = (df["squared_sum"]-2*df["avg"]*df["sum"]+df["avg"]**2)/df["count"]

    df["std"] = df["std"].apply(lambda x: x ** 0.5)

    # Calculate the match score from the std and the fairness

    df["match_score"] = df["std"] / df["fairness"] if df["fairness"] != 0 else 3

    # Return the df with the students ordered by the match score
    df = df[["student_id", "match_score", "best", "worst"]]
    df = df.drop_duplicates(subset=["student_id"], keep="first")
    df = df.sort_values(by="match_score", ascending=True)

    return df

def get_students_subject(student : Student, subject_code : str) -> Subject:
    return Subject.objects.all().filter(student=student, subject_code=subject_code).first()

def get_subjects(student : Student) -> set:

    return set(Subject.objects.all().filter(student=student).values_list('subject_code', flat=True))