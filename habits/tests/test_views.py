from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit


User = get_user_model()


class HabitViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="TestPassword123",
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="TestPassword123",
        )

        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            place="дома",
            time="08:00:00",
            action="делаю зарядку",
            is_pleasant=False,
            periodicity=1,
            reward="кофе",
            duration=60,
            is_public=False,
        )

        self.other_habit = Habit.objects.create(
            user=self.other_user,
            place="в спортзале",
            time="18:00:00",
            action="тренируюсь",
            is_pleasant=False,
            periodicity=1,
            reward="отдых",
            duration=60,
            is_public=False,
        )

    def get_habit_data(self, **kwargs):
        data = {
            "place": "дома",
            "time": "10:00:00",
            "action": "читаю книгу",
            "is_pleasant": False,
            "related_habit": None,
            "periodicity": 1,
            "reward": "кофе",
            "duration": 60,
            "is_public": False,
        }

        data.update(kwargs)
        return data

    def test_create_habit(self):
        url = reverse("habit-list")

        response = self.client.post(
            url,
            self.get_habit_data(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["action"], "читаю книгу")

    def test_user_is_assigned_automatically(self):
        url = reverse("habit-list")

        response = self.client.post(
            url,
            self.get_habit_data(
                action="новая привычка",
            ),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit = Habit.objects.get(id=response.data["id"])

        self.assertEqual(habit.user, self.user)

    def test_user_sees_only_own_habits(self):
        url = reverse("habit-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]

        habit_ids = [habit["id"] for habit in results]

        self.assertIn(self.habit.id, habit_ids)
        self.assertNotIn(self.other_habit.id, habit_ids)

    def test_user_can_retrieve_own_habit(self):
        url = reverse(
            "habit-detail",
            kwargs={"pk": self.habit.id},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.habit.id)

    def test_user_cannot_retrieve_other_users_habit(self):
        url = reverse(
            "habit-detail",
            kwargs={"pk": self.other_habit.id},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_habit(self):
        url = reverse(
            "habit-detail",
            kwargs={"pk": self.habit.id},
        )

        response = self.client.patch(
            url,
            {
                "action": "делаю зарядку утром",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["action"],
            "делаю зарядку утром",
        )

        self.habit.refresh_from_db()

        self.assertEqual(
            self.habit.action,
            "делаю зарядку утром",
        )

    def test_user_cannot_update_other_users_habit(self):
        url = reverse(
            "habit-detail",
            kwargs={"pk": self.other_habit.id},
        )

        response = self.client.patch(
            url,
            {
                "action": "изменённая привычка",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.other_habit.refresh_from_db()

        self.assertEqual(
            self.other_habit.action,
            "тренируюсь",
        )

    def test_user_can_delete_own_habit(self):
        url = reverse(
            "habit-detail",
            kwargs={"pk": self.habit.id},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(
            Habit.objects.filter(id=self.habit.id).exists()
        )

    def test_user_cannot_delete_other_users_habit(self):
        url = reverse(
            "habit-detail",
            kwargs={"pk": self.other_habit.id},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            Habit.objects.filter(id=self.other_habit.id).exists()
        )

    def test_public_habits_endpoint_returns_public_habits(self):
        public_habit = Habit.objects.create(
            user=self.other_user,
            place="парк",
            time="07:00:00",
            action="гуляю",
            is_pleasant=False,
            periodicity=1,
            reward="кофе",
            duration=60,
            is_public=True,
        )

        private_habit = Habit.objects.create(
            user=self.other_user,
            place="дома",
            time="12:00:00",
            action="отдыхаю",
            is_pleasant=False,
            periodicity=1,
            reward="",
            duration=60,
            is_public=False,
        )

        url = reverse("habit-public-habits")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]

        habit_ids = [habit["id"] for habit in results]

        self.assertIn(public_habit.id, habit_ids)
        self.assertNotIn(private_habit.id, habit_ids)

    def test_public_habits_can_be_seen_from_another_user(self):
        public_habit = Habit.objects.create(
            user=self.other_user,
            place="парк",
            time="07:00:00",
            action="гуляю",
            is_pleasant=False,
            periodicity=1,
            reward="кофе",
            duration=60,
            is_public=True,
        )

        url = reverse("habit-public-habits")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]

        habit_ids = [habit["id"] for habit in results]

        self.assertIn(public_habit.id, habit_ids)

    def test_habits_pagination(self):
        for number in range(6):
            Habit.objects.create(
                user=self.user,
                place="дома",
                time="10:00:00",
                action=f"привычка {number}",
                is_pleasant=False,
                periodicity=1,
                reward="кофе",
                duration=60,
                is_public=False,
            )

        url = reverse("habit-list")

        response = self.client.get(
            url,
            {
                "limit": 5,
                "offset": 0,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 7)
        self.assertEqual(len(response.data["results"]), 5)

        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

    def test_habits_pagination_second_page(self):
        for number in range(6):
            Habit.objects.create(
                user=self.user,
                place="дома",
                time="10:00:00",
                action=f"привычка {number}",
                is_pleasant=False,
                periodicity=1,
                reward="кофе",
                duration=60,
                is_public=False,
            )

        url = reverse("habit-list")

        response = self.client.get(
            url,
            {
                "limit": 5,
                "offset": 5,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 7)
        self.assertEqual(len(response.data["results"]), 2)

        self.assertIsNotNone(response.data["previous"])

    def test_unauthenticated_user_cannot_access_habits(self):
        self.client.force_authenticate(user=None)

        url = reverse("habit-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unauthenticated_user_cannot_create_habit(self):
        self.client.force_authenticate(user=None)

        url = reverse("habit-list")

        response = self.client.post(
            url,
            self.get_habit_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
