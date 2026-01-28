from django import forms
from .models import Test, Question

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'subject', 'start_time', 'end_time', 'total_marks', 'is_visible']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option', 'marks']
