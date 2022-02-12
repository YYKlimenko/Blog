from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, User



class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets={
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
                }
class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

