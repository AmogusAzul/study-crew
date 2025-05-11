from django.forms import ModelForm
from django import forms


from django.forms import inlineformset_factory
from .models import Student, Subject

SubjectFormSet = inlineformset_factory(
    Student, Subject,
    fields=('subject_code', 'score'),
    extra=1,            # how many blank forms to display
    can_delete=True     # allow deleting subjects
)