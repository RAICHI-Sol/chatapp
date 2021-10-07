from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup_view, name="signup_view"),
    path("login", views.Login.as_view(), name="login_view"),
    path("friends", views.friends, name="friends"),
    path("talk_room/<int:user_id>/", views.talk_room, name="talk_room"),
    path("setting", views.setting, name="setting"),
    path("username_change/",views.username_change,name ="username_change"),
    path("username_change_done/",views.username_change_done,name = "username_change_done"),
    path("mail_change/",views.mail_change,name ="mail_change"),
    path("mail_change_done/",views.mail_change_done,name = "mail_change_done"),
    path("password_change/", views.PasswordChange.as_view(), name="password_change"),
    path("password_change_done/", views.PasswordChangeDone.as_view(), name="password_change_done"), 
    path("logout",views.Logout.as_view(),name = "logout_view"),
]