from django import forms
from django.forms import Form

languages = [(1, "python")]

class CodeExecutorForm(Form):
    code = forms.CharField(widget=forms.Textarea, label='Code')
    language=forms.ChoiceField(choices=languages, label='Language')
