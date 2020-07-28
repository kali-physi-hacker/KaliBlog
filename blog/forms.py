from django import forms

from tinymce.widgets import TinyMCE

from .models import Comment, PostCategory, Post


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self):
        return False

class EmailPostForm(forms.Form):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentPostForm(forms.ModelForm):
    class Meta:
        fields = ("name", "email", "body")
        model = Comment


class PostCategoryForm(forms.ModelForm):
    class Meta:
        model = PostCategory
        fields = ('title', 'image')


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30, 'class':"form-control"}), max_length=250, required=False)
    class Meta:
        model = Post
        fields = ('title', 'author', 'body', 'image', 'status')
