from django.core.mail import send_mail

def send_activation_email(email, code):
    activation_url = f'http://localhost:8000/api/account/activate/?u={code}'

    send_mail(
        'Hello, activate your account',
        'To activate your account, go to this link:'
        f'\n{activation_url}',
        'nurdinov.d777@gmail.com',
        [email],
        fail_silently=False,
    )

def send_reset_password_email(email, code):
    send_mail(
        subject='Hello, reset your password',
        message=f'To reset your password, enter this code to the link: \n{code}',
        from_email='nurdinov.d777@gmail.com',
        recipient_list=[email],
        fail_silently=True,
    )