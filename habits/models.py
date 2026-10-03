from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
    )
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.TextField()
    is_pleasant = models.BooleanField(default=False)

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
    )

    periodicity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(7),
        ],
    )

    reward = models.TextField(blank=True)

    duration = models.PositiveIntegerField(
        default=120,
        validators=[
            MaxValueValidator(120),
        ],
    )

    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение "
                "и связанную привычку."
            )

        if self.duration > 120:
            raise ValidationError(
                "Время выполнения не может превышать 120 секунд."
            )

        if not 1 <= self.periodicity <= 7:
            raise ValidationError(
                "Периодичность должна быть от 1 до 7 дней."
            )

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(
                "Связанная привычка должна быть приятной."
            )

        if self.is_pleasant and (
            self.reward or self.related_habit
        ):
            raise ValidationError(
                "У приятной привычки не может быть "
                "вознаграждения или связанной привычки."
            )

    def __str__(self):
        return self.action
