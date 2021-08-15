from django import forms

from .models import Question, Answer


class MCForm(forms.Form):
    choice = forms.CharField()


class TextForm(forms.Form):
    ans = forms.CharField(max_length=50)


class FileForm(forms.Form):
    file = forms.FileField()


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50)
