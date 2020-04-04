from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import article, author, category, comment

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class createUserPost(forms.ModelForm):
    class Meta:
        model = article
        fields = [
            'title',
            'body',
            'image',
            'category'
        ]

class createUserProfile(forms.ModelForm):
    class Meta:
        model = author
        fields = ['profile_picture', 'datails']

class userCommentForm(forms.ModelForm):
    class Meta:
        model  = comment
        fields = [
            'name',
            'email',
            'post_comment'
        ] 
