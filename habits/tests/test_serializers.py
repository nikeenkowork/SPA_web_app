from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.serializers import HabitSerializer


User = get_user_model()


class HabitSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="TestPassword123",
        )

        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="дома",
            time="08:00:00",
            action="пью кофе",
            is_pleasant=True,
            periodicity=1,
            reward="",
            duration=60,
        )

        self.normal_habit = Habit.objects.create(
            user=self.user,
            place="дома",
            time="09:00:00",
            action="делаю зарядку",
            is_pleasant=False,
            periodicity=1,
            reward="кофе",
            duration=60,
        )

    def get_data(self, **kwargs):
        data = {
            "place": "дома",
            "time": "10:00:00",
            "action": "читаю книгу",
            "is_pleasant": False,
            "related_habit": None,
            "periodicity": 1,
            "reward": "",
            "duration": 60,
            "is_public": False,
        }
        data.update(kwargs)
        return data

    def test_reward_and_related_habit_are_forbidden_together(self):
        serializer = HabitSerializer(
            data=self.get_data(
                related_habit=self.pleasant_habit.id,
                reward="кофе",
            )
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("Нельзя одновременно указывать", str(serializer.errors))

    def test_duration_cannot_exceed_120_seconds(self):
        serializer = HabitSerializer(
            data=self.get_data(duration=121)
        )

        self.assertFalse(serializer.is_valid())

    def test_periodicity_must_be_from_1_to_7(self):
        serializer = HabitSerializer(
            data=self.get_data(periodicity=8)
        )

        self.assertFalse(serializer.is_valid())

    def test_related_habit_must_be_pleasant(self):
        serializer = HabitSerializer(
            data=self.get_data(
                related_habit=self.normal_habit.id,
            )
        )

        self.assertFalse(serializer.is_valid())

    def test_pleasant_habit_cannot_have_reward(self):
        serializer = HabitSerializer(
            data=self.get_data(
                is_pleasant=True,
                reward="кофе",
            )
        )

        self.assertFalse(serializer.is_valid())

    def test_pleasant_habit_cannot_have_related_habit(self):
        serializer = HabitSerializer(
            data=self.get_data(
                is_pleasant=True,
                related_habit=self.pleasant_habit.id,
            )
        )

        self.assertFalse(serializer.is_valid())

    def test_valid_habit_is_accepted(self):
        serializer = HabitSerializer(
            data=self.get_data(
                reward="кофе",
                duration=120,
                periodicity=7,
            )
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
