from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Posts
from django import forms
from .models import Comments, MessageModel


#/register allow user to register for site
class RegisterForm(UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = User
        fields = ['username','password1', 'password2']




#The Form for actually typing and submitting a post
class PostForm(ModelForm):
    body = forms.CharField( required=True, widget=forms.widgets.Textarea(attrs={'placeholder':'Post Something....', 'class': 'textarea is-success is-medium'}), label="")
    class Meta:
        model = Posts
        fields = ['body']


#The form for actually typing a comment and submitting it on a post
class CommentForm(ModelForm):
    comment_content = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'placeholder':'Comment Something....', 'class':'textarea is-success is-medium'}), label="")

    class Meta:
        model = Comments
        fields = ['comment_content']




class ThreadForm(forms.Form): #form for creating a thread with another user
    username = forms.CharField(label='', max_length=100)



class MessageForm(forms.Form):
    message = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={'placeholder': 'Write message here....', 'class': 'textarea is-success is-medium'}), label="")





