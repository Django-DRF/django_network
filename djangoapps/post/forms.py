from django import forms
from django.contrib.auth.models import User

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
