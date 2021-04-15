from django import forms
from .models import UserData, Note


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    class Meta:
        model = UserData
        fields = ['username', 'password']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text']   

        