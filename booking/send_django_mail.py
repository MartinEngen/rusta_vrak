
from django.core.mail import send_mail

send_mail(
    'subject',
    'Message',
    'Nitrax92@gmail.com', #From
    ['Martin.Engen@outlook.com'],
    fail_silently=False,
)