# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signin/', siginin, name="signin"),
    path('login/', login_user, name="login"),
    path('signup/', signup, name="signup"),
    path('register/', register_user, name="register"),
    path("logout/", getlogout, name="logout"),
    path('forgot_password/', forgot_password, name="forgot password"),
    path('reset_password_mail/', reset_password_mail, name="reset password mail"),
    path('reset_password/<slug:hashval>', reset_password),
    path('change_password/', change_password, name='change password'),
]
