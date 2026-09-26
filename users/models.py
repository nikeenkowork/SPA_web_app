from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from materials.models import Course, Lesson


class CustomUserManager(BaseUserManager):
    """Менеджер пользователей с авторизацией по email."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")

        if not extra_fields.get("is_superuser"):
            raise ValueError(
                "Суперпользователь должен иметь is_superuser=True."
            )

        return self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Модель платежа пользователя."""

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Наличные"
        TRANSFER = "transfer", "Перевод на счет"
        STRIPE = "stripe", "Stripe"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )

    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный курс",
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный урок",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",
    )

    payment_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
    )

    stripe_session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Stripe Session ID",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        verbose_name="Способ оплаты",
    )

    def __str__(self):
        return f"{self.user.email} — {self.amount}"


class Subscription(models.Model):
    """Подписка пользователя на обновления курса."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Курс",
    )

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.email} — {self.course.name}"
