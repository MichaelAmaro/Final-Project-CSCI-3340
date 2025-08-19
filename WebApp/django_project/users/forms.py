from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, help_text='Enter your full name')
    email = forms.EmailField(
        help_text='Please use your UTRGV email address (@utrgv.edu)'
    )

    class Meta: 
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2'] # this is the order of the fields in the form

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@utrgv.edu'):
            raise forms.ValidationError('Only UTRGV email addresses (@utrgv.edu) are allowed for registration.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Store the full name in the first_name field
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user


