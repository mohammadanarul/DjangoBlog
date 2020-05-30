from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import article, author, category, Comment

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
        fields = ['profile_picture', 'profile_background_picture', 'datails']

class createCategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = [ 'name', ]
            
        

class userCommentForm(forms.ModelForm):
    post_comment = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Reply comment content', 'rows': '4', 'cols': '50' }))
    class Meta:
        model  = Comment
        fields = [
            'post_comment'
        ] 
