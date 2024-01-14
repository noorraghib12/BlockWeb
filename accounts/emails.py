from django.core.mail import send_mail
from uuid import uuid4
from django.conf import settings
from .models import User

def send_uuid_email(email):
    subject= "Blockstak Website Registration token"
    auth_string=str(uuid4())
    message= f"Thank you for applying to Blockstak. Here is your registration key:{auth_string}"    
    email_from=settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    user_obj=User.objects.get(email=email)
    user_obj.email_verify_token=auth_string
    user_obj.save()


