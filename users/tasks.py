from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def test_task():
    return "Celery task works!"


@shared_task
def deactivate_inactive_users():
    """Блокирует пользователей, которые не входили более месяца."""

    User = get_user_model()

    threshold = timezone.now() - timedelta(days=30)

    users = User.objects.filter(
        last_login__lt=threshold,
        is_active=True,
    )

    count = users.update(is_active=False)

    return f"Заблокировано пользователей: {count}"
