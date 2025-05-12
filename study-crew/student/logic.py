from django.db.models.query import QuerySet

from student.models import Student, Subject

from django.contrib.auth.models import User

import pandas as pd

def search_matches_by_subjects(student : Student, use_subjects : bool = False, subject_codes : set = set()) -> pd.DataFrame:

    if not use_subjects:
        
        subject_codes = get_subjects(student)

    df = pd.DataFrame(columns=["student_id",
                                "fairness",
                                "sum", 
                                "count",
                                "best_id", "best_score",
                                "worst_id", "worst_score",
                                  "squared_sum"])

    excluded_contacts = student.user.contact.blocked_students.all() | student.user.contact.friends.all()

    excluded_users = User.objects.filter(
        contact__in=excluded_contacts
    ).exclude(
        id=student.user.id
    )

    # Convert those to STUDENTS
    excluded_students = Student.objects.filter(user__in=excluded_users)

    # Fetch relevant subjects
    subjects = Subject.objects.filter(
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

            df = df._append({
                "student_id": student_id,
                "fairness": subject_delta,
                "sum": abs(subject_delta),
                "count": 1,
                "best_id": entry.id,
                "best_score": entry.score,
                "worst_id": entry.id,
                "worst_score": entry.score,
                "squared_sum": subject_delta ** 2
            }, ignore_index=True)
        else:

            curr_fairness = df[df["student_id"] == student_id]["fairness"].values[0]
            curr_sum = df[df["student_id"] == student_id]["sum"].values[0]
            curr_count = df[df["student_id"] == student_id]["count"].values[0]
            curr_best_id = df[df["student_id"] == student_id]["best"].values[0]
            curr_worst_id = df[df["student_id"] == student_id]["worst"].values[0]
            curr_squared_sum = df[df["student_id"] == student_id]["squared_sum"].values[0]

            curr_best_score = df[df["student_id"] == student_id]["best_score"].values[0]
            curr_worst_score = df[df["student_id"] == student_id]["worst_score"].values[0]

            df.loc[df["student_id"] == student_id, "fairness"] = curr_fairness + subject_delta
            df.loc[df["student_id"] == student_id, "sum"] = curr_sum + abs(subject_delta)
            df.loc[df["student_id"] == student_id, "count"] = curr_count + 1
            df.loc[df["student_id"] == student_id, "squared_sum"] = curr_squared_sum + (subject_delta ** 2)

            if entry.score > curr_best_score:
                df.loc[df["student_id"] == student_id, "best_score"] = entry.score
                df.loc[df["student_id"] == student_id, "best_id"] = entry.id

            if entry.score < curr_worst_score:
                df.loc[df["student_id"] == student_id, "worst_score"] = entry.score
                df.loc[df["student_id"] == student_id, "worst_id"] = entry.id

    # Calculate abs of the fairness
    df["fairness"] = df["fairness"].apply(lambda x: abs(x))

    df["avg"] = df["sum"] / df["count"]

    df["std"] = (df["squared_sum"]-2*df["avg"]*df["sum"]+df["avg"]**2)/df["count"]

    df["std"] = df["std"].apply(lambda x: x ** 0.5)

    # Calculate the match score from the std and the fairness

    df["match_score"] = df.apply(
        lambda row: row["std"] / row["fairness"] if row["fairness"] != 0 else 3,
        axis=1
    )

    # Return the df with the students ordered by the match score
    df = df[["student_id", "match_score", "best_id", "worst_id"]]
    df = df.drop_duplicates(subset=["student_id"], keep="first")
    df = df.sort_values(by="match_score", ascending=True)

    return df

def get_students_subject(student : Student, subject_code : str) -> Subject:
    return Subject.objects.all().filter(student=student, subject_code=subject_code).first()

def get_subjects(student : Student) -> set:

    return set(Subject.objects.all().filter(student=student).values_list('subject_code', flat=True))