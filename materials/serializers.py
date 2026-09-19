from rest_framework import serializers

from users.models import Payment, Subscription

from .models import Course, Lesson
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели урока."""

    video_url = serializers.URLField(
        validators=[validate_youtube_url],
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курса."""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        ]

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе."""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет подписку текущего пользователя на курс."""

        user = self.context["request"].user

        if not user.is_authenticated:
            return False

        return Subscription.objects.filter(
            user=user,
            course=obj,
        ).exists()


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели платежа."""

    class Meta:
        model = Payment
        fields = "__all__"
