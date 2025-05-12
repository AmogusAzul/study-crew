from django.forms import ModelForm
from django import forms

from django.forms.models import BaseInlineFormSet

from django.forms import inlineformset_factory
from .models import Student, Subject

from django.core.exceptions import ValidationError

class BaseSubjectFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        seen = set()
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            code = form.cleaned_data.get('subject_code')
            if code in seen:
                raise ValidationError("Subjects must be unique per student.")
            seen.add(code)

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_code', 'score']
        widgets = {
            'subject_code': forms.TextInput(attrs={'placeholder': 'Subject Code'}),
            'score': forms.NumberInput(attrs={
            'type': 'range',
            'min': 1,
            'max': 10,
            'step': 1,
            'class': 'form-range'
        }),
        }
        labels = {
            'subject_code': '',
            'score': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable subject_code only for existing objects (not the extra empty form)
        if self.instance and self.instance.pk:
            self.fields['subject_code'].disabled = True

SubjectFormSet = inlineformset_factory(
    Student, Subject,
    formset=BaseSubjectFormSet,
    form=SubjectForm,
    fields=('subject_code', 'score'),
    extra=1,            # how many blank forms to display
    can_delete=True     # allow deleting subjects
)