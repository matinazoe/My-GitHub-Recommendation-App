from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User

from .models import Review, UserProfile

# User Forms
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
		
class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
		

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('company', 'location', 'type')
		


# Project Forms

# Review Forms
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title','comment','status']
        widgets = {
            'comment': Textarea(attrs={'cols': 40, 'rows': 15})
        }

