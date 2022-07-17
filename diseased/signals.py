from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DiseasedUser, StatusDiseasedUser


@receiver(post_save, sender=DiseasedUser)
def send_request_email(sender, instance, created, **kwargs):
    subject = f"An application was received from the {instance.telephone_number} phone number !"
    message = """ 
            Your application has been accepted, please
            expect response, or check spam we may have sent you a reply!
            """
    if instance.email_address and created:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email_address]
        )


@receiver(post_save, sender=StatusDiseasedUser)
def send_response_email(sender, instance, created, **kwargs):
    subject = f"{instance.diseased.telephone_number} telephone number's application has been responded!"
    if instance.status == instance.StatusType.ACCEPT:
        message = f""" 
        Your application has been accepted.
        Your doctor: {instance.doctor.full_name}, your doctor's telephone number: {instance.doctor.tel_number}.
        Additional Information: {instance.comment}.
        """
    else:
        message = """ 
        Your application has not been accepted, there can be various reasons for this,
        for example: that no more detailed information has been provided.
        Please leave us another application or contact us.
        our phone number: +998901234567
        """

    if instance.diseased.email_address and created:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.diseased.email_address]
        )
