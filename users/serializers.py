from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone",
            "city",
            "avatar",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "phone",
            "city",
            "avatar",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class PaymentCreateSerializer(serializers.Serializer):
    """Запрос на создание платежа."""

    course = serializers.IntegerField(
        help_text="ID курса, который необходимо оплатить.",
    )


class PaymentCreateResponseSerializer(serializers.Serializer):
    """Ответ после создания платежа."""

    payment_id = serializers.IntegerField()
    payment_url = serializers.URLField()
    session_id = serializers.CharField()


class SubscriptionSerializer(serializers.Serializer):
    """Запрос на добавление или удаление подписки."""

    course = serializers.IntegerField(
        help_text="ID курса.",
    )


class SubscriptionResponseSerializer(serializers.Serializer):
    """Ответ операции с подпиской."""

    message = serializers.CharField()