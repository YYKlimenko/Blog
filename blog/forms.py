from django import forms
from .models import Comment


class AddCommentForm(forms.ModelForm):


    def save(self, post_id, is_authenticated, request, *user_id, commit=True):
        form = super().save(commit=False)
        form.post_id = post_id
        if is_authenticated:
            form.author_id = user_id
        parent = request.POST.get('parent')
        if parent:
                form.parent_id = anchor = parent
        else:
                anchor = 'comments'
        print(form)
        return super().save()

    class Meta:
        model = Comment
        fields = ['text']
        widgets={
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
                }



