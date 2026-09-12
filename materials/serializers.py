from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели урока."""

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
