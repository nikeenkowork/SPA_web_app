from rest_framework import serializers

from .models import Course, Lesson
from users.models import Payment
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

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "description",
            "lessons_count",
            "lessons",
        ]

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе."""
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели платежа."""

    class Meta:
        model = Payment
        fields = "__all__"
