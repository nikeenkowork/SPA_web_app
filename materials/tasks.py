from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_course_update_email(email, course_name):
    """Отправляет письмо об обновлении курса."""

    send_mail(
        subject=f"Обновление курса: {course_name}",
        message=(
            f"Курс «{course_name}» был обновлен.\n\n"
            "Зайдите на платформу, чтобы ознакомиться с изменениями."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
