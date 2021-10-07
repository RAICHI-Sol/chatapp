import django
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm # 追加
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView
from django.contrib.auth.decorators import login_required  # 追加
from django.urls import reverse_lazy # 追加
from django.contrib.auth.models import User  # User モデルを追加
from main.models import User #こちらのコードを追加
from .models import Talk # Talk を追加
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .forms import (
    SignUpForm,
    LoginForm,
    TalkForm,
    UserNameSettingForm,
    MailSettingForm,
)
from .models import User

def index(request):
    return render(request, "main/index.html")

def signup_view(request):

    if request.method == "GET":
        form = SignUpForm()

    elif request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("/")
    context = {"form": form}
    return render(request, "main/signup.html", context)

class Login(LoginView):
    authentication_form = LoginForm
    template_name       = "main/login.html"

class Logout(LoginRequiredMixin, LogoutView):
    pass

def talk_room(request, user_id):
    user = request.user
    friend = get_object_or_404(User,id=user_id)
    talk    = Talk.objects.filter(Q(talk_from =user,talk_to=friend) | Q(talk_to=user,talk_from = friend))
    talk    = talk.order_by("time")

    form = TalkForm()
    context = {
        "form":form,
        "talk":talk,
    }

    if request.method == "POST":
        form = TalkForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("talk")
            new_talk =  Talk(talk = text,talk_from=user,talk_to=friend)
            new_talk.save()
            return render(request,"main/talk_room.html",context)
    return render(request,"main/talk_room.html",context)
    
@login_required
def friends(request):
    user = request.user
    friends = User.objects.exclude(id=user.id)
    context = {
        "friends": friends,
    }
    return render(request, "main/friends.html", context)

@login_required
def setting(request):
    return render(request, "main/setting.html")


@login_required
def username_change(request):
    user = request.user
    if request.method == "GET":
        form = UserNameSettingForm(instance=user)
    
    elif request.method == "POST":
        form = UserNameSettingForm(request.POST,instance = user)
        if form.is_valid():
            form.save()
            return redirect("username_change_done")
    
    context ={
        "form":form,
    }
    return render(request,"main/username_change.html",context)


@login_required
def username_change_done(request):
    return render(request,"main/username_change_done.html")

@login_required
def mail_change(request):
    user = request.user
    if request.method == "GET":
        form = MailSettingForm(instance=user)

    elif request.method == "POST":
        form = MailSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return  redirect("mail_change_done")

    context = {
        "form":form,
    }
    return render(request,"main/mail_change.html",context)


@login_required
def mail_change_done(request):
    return render(request, "main/mail_change_done.html")

class PasswordChange(PasswordChangeView):
    form_class    = PasswordChangeForm
    success_url   = reverse_lazy("password_change_done")
    template_name = "main/password_change.html"

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = "main/password_change_done.html"