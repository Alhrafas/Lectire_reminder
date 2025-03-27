from django import forms
from .models import Lecture
from django.contrib.auth.models import User

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'date', 'time', 'venue', 'reminder_time', 'is_recurring', 'category']
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "reminder_time": forms.TimeInput(attrs={"type": "time"}),
            "category": forms.Select(),  # Dropdown for categories
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full border-gray-600 rounded-lg p-3', 'placeholder': 'Enter password'})
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full border-gray-600 rounded-lg p-3', 'placeholder': 'Confirm password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full border-gray-600 rounded-lg p-3', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border-gray-600 rounded-lg p-3', 'placeholder': 'Enter email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
