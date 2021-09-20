from django import forms
from django.forms import ModelForm, Form

from .models import Question, Answer


class MCForm(Form):
    choice = forms.CharField()
    correct = forms.CharField()


class TextForm(Form):
    ans = forms.CharField(max_length=50)
    correct = forms.CharField()

class FileForm(Form):
    file = forms.FileField()


class SearchForm(Form):
    search = forms.CharField(max_length=50)


class QuestionForm(ModelForm):
    question_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'text-ans auto-width', 'autocomplete': 'off'}))

    class Meta:
        model = Question
        fields = ['question_text']


class AnswerForm(ModelForm):
    answer_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'text-ans auto-width', 'autocomplete': 'off'}))

    class Meta:
        model = Answer
        fields = ['answer_text']
