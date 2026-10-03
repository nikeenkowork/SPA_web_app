from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["id", "user"]

    def validate(self, attrs):
        reward = attrs.get("reward")
        related_habit = attrs.get("related_habit")
        is_pleasant = attrs.get("is_pleasant", False)
        duration = attrs.get("duration", 120)
        periodicity = attrs.get("periodicity", 1)

        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение "
                "и связанную привычку."
            )

        if duration > 120:
            raise serializers.ValidationError(
                "Время выполнения не может превышать 120 секунд."
            )

        if not 1 <= periodicity <= 7:
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 дней."
            )

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной."
            )

        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть "
                "вознаграждения или связанной привычки."
            )

        return attrs
