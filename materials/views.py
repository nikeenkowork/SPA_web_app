from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from users.filters import PaymentFilter
from users.models import Payment
from users.permissions import IsModerator

from .models import Course, Lesson
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    PaymentSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD курсов."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve",
            "update",
            "partial_update",
        ]:
            permission_classes = [IsAuthenticated, IsModerator]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class LessonListCreateView(generics.ListCreateAPIView):
    """Список и создание уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated, IsModerator]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, изменение и удаление урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "PATCH"]:
            permission_classes = [IsAuthenticated, IsModerator]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class PaymentListView(generics.ListAPIView):
    """Список платежей."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_class = PaymentFilter

    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]
