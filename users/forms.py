from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_group = forms.ChoiceField(choices=Profile.USER_GROUPS, required=True, label="User Group")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.profile.user_group = self.cleaned_data['user_group']
            user.profile.save()
        return user
        
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_group']