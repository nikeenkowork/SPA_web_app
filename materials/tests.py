from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import Subscription, User


class LessonAPITests(APITestCase):
    """Тесты CRUD и прав доступа для уроков."""

    def setUp(self):
        """Создание тестовых данных."""

        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpassword123",
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="testpassword123",
        )

        self.moderator = User.objects.create_user(
            email="moderator@example.com",
            password="testpassword123",
        )

        moderators_group, _ = Group.objects.get_or_create(
            name="Модераторы",
        )
        self.moderator.groups.add(moderators_group)

        self.course = Course.objects.create(
            name="Python курс",
            description="Курс по Python",
            owner=self.user,
        )

        self.lesson = Lesson.objects.create(
            course=self.course,
            name="Урок 1",
            description="Введение в Python",
            video_url="https://www.youtube.com/watch?v=test123",
            owner=self.user,
        )

        self.lessons_url = "/api/lessons/"

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "course": self.course.id,
            "name": "Урок 2",
            "description": "Новый урок",
            "video_url": "https://www.youtube.com/watch?v=test456",
        }

        response = self.client.post(
            self.lessons_url,
            data,
            format="json",
        )

        print("STATUS:", response.status_code)
        print("DATA:", response.data)

    def test_create_lesson_unauthenticated(self):
        """Неавторизованный пользователь не может создать урок."""

        data = {
            "course": self.course.id,
            "name": "Урок 2",
            "description": "Новый урок",
            "video_url": "https://www.youtube.com/watch?v=test456",
        }

        response = self.client.post(
            self.lessons_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_retrieve_own_lesson(self):
        """Владелец может просматривать свой урок."""

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"{self.lessons_url}{self.lesson.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["id"],
            self.lesson.id,
        )

    def test_retrieve_other_user_lesson(self):
        """Другой пользователь не может просматривать чужой урок."""

        self.client.force_authenticate(user=self.other_user)

        response = self.client.get(
            f"{self.lessons_url}{self.lesson.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_moderator_can_retrieve_lesson(self):
        """Модератор может просматривать чужой урок."""

        self.client.force_authenticate(user=self.moderator)

        response = self.client.get(
            f"{self.lessons_url}{self.lesson.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_own_lesson(self):
        """Владелец может изменить свой урок."""

        self.client.force_authenticate(user=self.user)

        data = {
            "name": "Измененный урок",
        }

        response = self.client.patch(
            f"{self.lessons_url}{self.lesson.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.lesson.refresh_from_db()

        self.assertEqual(
            self.lesson.name,
            "Измененный урок",
        )

    def test_update_other_user_lesson(self):
        """Другой пользователь не может изменить чужой урок."""

        self.client.force_authenticate(user=self.other_user)

        data = {
            "name": "Чужой измененный урок",
        }

        response = self.client.patch(
            f"{self.lessons_url}{self.lesson.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )


    def test_delete_own_lesson(self):
        """Владелец может удалить свой урок."""

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f"{self.lessons_url}{self.lesson.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.filter(id=self.lesson.id).exists(),
        )

    def test_delete_other_user_lesson(self):
        """Другой пользователь не может удалить чужой урок."""

        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(
            f"{self.lessons_url}{self.lesson.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
