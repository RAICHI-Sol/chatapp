from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from main.models import User #こちらのコードを追加
from django.core.exceptions import ValidationError #追加部分

TABOO_WORDS = [
    "ばか",
    "バカ",
    "あほ",
    "アホ",
]


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

    def clean(self):
        cleaned_data = super().clean()
        talk = cleaned_data.get("talk")
        contained_taboo_words = [w for w in TABOO_WORDS if w in talk]
        if contained_taboo_words:
            raise ValidationError(f"禁止ワード {', '.join(contained_taboo_words)} が含まれています")
        return cleaned_data

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