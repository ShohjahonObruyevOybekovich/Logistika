from celery import shared_task

from django.core.mail import send_mail


@shared_task
def send_forget_password(email, reset_link):
    send_mail(
        'Password Reset',
        f'Click the following link to reset your password:   {reset_link}',
        'from@example.com',
        [email],
        fail_silently=False,
    )
    return "Done"


@shared_task
def send_email(email, confirmation_code):
    send_mail(
        'Registration Confirmation Code',
        f'Your confirmation code is: {confirmation_code}',
        'from@example.com',
        [email],
        fail_silently=False,
    )
