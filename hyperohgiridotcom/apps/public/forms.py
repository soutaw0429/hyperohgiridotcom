from django import forms
from hyperohgiridotcom.apps.accounts.models import Post, Comment



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_image' ,'content']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ContactForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', max_length=254, required=True)
    content = forms.CharField(label='お問合せ内容', required=True)