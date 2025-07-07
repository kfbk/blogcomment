from django import forms
from .models import Comment
""" markdownx追記 """
from .models import Post
from markdownx.widgets import MarkdownxWidget 

class BlogForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'thumbnail')
        widgets = {
                'content': MarkdownxWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
        }