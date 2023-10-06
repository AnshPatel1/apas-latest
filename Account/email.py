from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

from APAS.settings import *
from django.template.loader import render_to_string


@csrf_exempt
def send_password_reset_mail(pass_reset_request, request):
    subject = 'APAS 3 - Password Reset'
    message = render_to_string('includes/reset-password-email-template.html', {'name': pass_reset_request.user.full_name,
                                                                               'username': pass_reset_request.user.username,
                                                                               'token': pass_reset_request.token}, request=request)
    plain_message = strip_tags(message)
    from_email = EMAIL_HOST_USER
    if subject and message and from_email:
        try:
            send_mail(subject, plain_message, from_email, [pass_reset_request.user.email], html_message=message)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return True
