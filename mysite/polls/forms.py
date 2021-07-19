from django import forms


class MCForm(forms.Form):
    choice = forms.CharField()


class TextForm(forms.Form):
    ans = forms.CharField()


class FileForm(forms.Form):
    file = forms.FileField()