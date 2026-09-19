from django.core.exceptions import ValidationError


def validate_youtube_url(value):
    """Проверяет, что ссылка ведет на YouTube."""

    if "youtube.com" not in value and "youtu.be" not in value:
        raise ValidationError(
            "Разрешены только ссылки на YouTube."
        )
