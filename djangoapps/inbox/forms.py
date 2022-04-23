from django import forms
from django.contrib.auth.models import User

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
