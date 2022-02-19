from django import forms
from .models import Comment


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets={
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
                }


class SearchForm(forms.Form):
    text = forms.CharField(max_length=50)


