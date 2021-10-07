from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from main.models import User #こちらのコードを追加

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)

class LoginForm(AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "fomr-control"

class TalkForm(forms.Form):
    talk = forms.CharField(label="talk")

class UserNameSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username":"新しいユーザー名"}

class MailSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
    
    def __int__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["email"].label = "新しいメールアドレス"