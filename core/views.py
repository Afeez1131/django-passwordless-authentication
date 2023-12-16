from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.conf import settings
from .models import UserToken
from django.core.signing import BadSignature
from django.contrib.auth import login, logout

def homepage(request):

    return render(request, 'core/homepage.html', {})


def one_time_login(request):
    if request.method == 'POST':
        mail = request.POST.get('email', '')
        try:
            user = User.objects.get(email=mail)
        except User.DoesNotExist:
            return HttpResponse('Provided mail is not for a valid user')
        token = default_token_generator.make_token(user)
        create_user_token(user, token)
        login_link = request.build_absolute_uri(reverse('password:passwordless_login', args=[token]))
        subject = 'One Time Login Link'
        message = format_html(
            f"Hello {user.username},<br><br>Please click on the following link to login to your account:<br><br><a href='{login_link}'>{login_link}</a><br><br>This link is only valid once.<br><br>Sincerely,<br>The Team")

        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
        return HttpResponse(f"One time login sent to {mail}")
    return render(request, 'core/one_time_login.html', {})


def create_user_token(user, token):
    try:
        user_token = UserToken.objects.get(user=user)
    except UserToken.DoesNotExist:
        user_token = UserToken.objects.create(user=user)
    user_token.token=token
    user_token.save()
    return


def passwordless_login(request, token):
    try:
        user_token = UserToken.objects.get(token=token)
    except UserToken.DoesNotExist:
        return HttpResponse("invalid request")
    try:
        if token and default_token_generator.check_token(user_token.user, token):
            login(request, user_token.user)
        else:
            return HttpResponse("invalid request")
    except (User.DoesNotExist, BadSignature):
        return HttpResponse("invalid token")
    return HttpResponseRedirect(reverse('password:home'))