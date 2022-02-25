from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from home.models import Profile, Post, Comment, Author


class EditProfileForm(ModelForm):
    bio = forms.TextInput()
    facebook_url = forms.CharField()
    instagram_url = forms.CharField()
    linkedin_url = forms.CharField()
    picture = forms.ImageField()

    class Meta:
        model = Profile
        fields = (
        'bio',
        'picture',
        'facebook_url',
        'instagram_url',
        'linkedin_url'
        )

class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2' )

class EditUserForm(UserChangeForm):
    password = None
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username','last_name', 'first_name','email')
