from rest_framework import serializers

# Импортируем модели курса и урока
from .models import Course, Lesson


# Сериализатор для модели Course
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        # С какой моделью работает сериализатор
        model = Course

        # Использовать все поля модели
        fields = "__all__"


# Сериализатор для модели Lesson
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        # С какой моделью работает сериализатор
        model = Lesson

        # Использовать все поля модели
        fields = "__all__"
