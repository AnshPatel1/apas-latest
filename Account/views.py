from django.http import HttpResponse
from django.shortcuts import render
from Account.models import User, PasswordReset, DualRole
from Account.email import send_password_reset_mail


# Create your views here.

def login(request):
    return render(request, "include/login.html", {})


def forgot_password(request):
    if request.method == "GET" and not request.user.is_authenticated:
        return render(request, "includes/forgot_password.html", {})
    if request.method == "POST" and not request.user.is_authenticated:
        email = request.POST.get("email")
        try:
            context = {}
            account = User.objects.get(email__iexact=email)
            context['found'] = True
            context['email'] = account.email[0:3] + len(account.email[4:-4]) * '*' + account.email[-4:]
            context['is_post'] = True
            pr = PasswordReset()
            pr.user = account
            pr.save()
            if send_password_reset_mail(pr, request):
                context['found'] = True
                context['email'] = account.email[0:3] + len(account.email[4:-4]) * '*' + account.email[-4:]
                context['is_post'] = True
                return render(request, "includes/forgot_password.html", context)
        except User.DoesNotExist:
            context = {'found': False, 'msg': 'No account found with this email', 'is_post': True}
            return render(request, "includes/forgot_password.html", context)


def password_reset(request):
    if request.method == "GET" and not request.user.is_authenticated:
        token = request.GET.get("token")
        try:
            pr = PasswordReset.objects.get(token=token)
            context = {'token': token}
            return render(request, "includes/reset-password.html", context)
        except PasswordReset.DoesNotExist:
            return HttpResponse("Invalid token")
    if request.method == "POST" and not request.user.is_authenticated:
        password = request.POST.get("password")
        token = request.POST.get("token")
        try:
            pr = PasswordReset.objects.get(token=token)
            pr.user.set_password(password)
            pr.user.save()
            try:
                alt_user = DualRole.objects.get(main_user=pr.user)
                alt_user.faculty_profile.set_password(password)
                alt_user.faculty_profile.save()
            except DualRole.DoesNotExist:
                pass

            pr.delete()
            return render(request, "includes/reset-password.html", {'success': True})
        except PasswordReset.DoesNotExist:
            return HttpResponse("Invalid token")
