import random
import string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

User = get_user_model()

def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_otp_email(email, otp):

    context = {
        'full_name': User.objects.get(email=email),
        'reset_password_otp': otp
    }
    email_html_message = render_to_string('accounts/password_reset_email.html', context)
    email_plaintext_message = render_to_string('accounts/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        'Password Reset for {title}'.format(title='Med Adherence'),
        # message:
        email_plaintext_message,
        # from:
        settings.DEFAULT_FROM_EMAIL,
        # to:
        [email]
    )
    msg.attach_alternative(email_html_message, 'text/html')
    msg.send()