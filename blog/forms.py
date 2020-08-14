from django import forms

from .models import Comment, PostCategory, Post


class EmailPostForm(forms.Form):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentPostForm(forms.ModelForm):
    class Meta:
        fields = ("body",)
        model = Comment


class PostCategoryForm(forms.ModelForm):
    class Meta:
        model = PostCategory
        fields = ('title', 'image')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'body', 'image', 'status', 'tags')
