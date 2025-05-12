from django.core.paginator import Paginator
from django.shortcuts import render
from student.models import Student
from student.logic import search_matches_by_subjects
from django.contrib.auth.decorators import login_required

from student.models import Subject

def search_view(request):
    student = request.user.student  # Assuming OneToOneField to User

    df = search_matches_by_subjects(student)  # Your custom function

    match_list = []
    for _, row in df.iterrows():
        try:
            match_student = Student.objects.select_related("user").get(pk=row["student_id"])
            match_list.append({
                "student": match_student,
                "match_score": row["match_score"],
                "best": Subject.objects.filter(id=row["best_id"]).first(),
                "worst": Subject.objects.filter(id=row["worst_id"]).first(),
            })
        except Student.DoesNotExist:
            continue  # skip rows that don't match a real student

    paginator = Paginator(match_list, 10)  # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/search.html', {
        'page_obj': page_obj,
    })