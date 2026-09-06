from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название",
    )
    preview = models.ImageField(
        upload_to="courses/previews/",
        blank=True,
        null=True,
        verbose_name="Превью",
    )
    description = models.TextField(
        verbose_name="Описание",
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    preview = models.ImageField(
        upload_to="lessons/previews/",
        blank=True,
        null=True,
        verbose_name="Превью",
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
    )

    def __str__(self):
        return self.name
